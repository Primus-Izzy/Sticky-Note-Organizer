"""
Note categorization and organization logic.

Keywords are matched on word boundaries with light suffix stemming
(e.g. "business" also matches "businesses", "invest" matches "investing"),
so short keywords no longer misfire on substrings ("do" vs "download").
Strong signals (currency amounts, URLs, code snippets) add weighted boosts;
contact details (phone numbers, emails) take priority outright.
"""

import re
from collections import defaultdict
from functools import lru_cache
from typing import List, Dict, Any


@lru_cache(maxsize=2048)
def _keyword_pattern(keyword: str):
    """Compile a word-boundary pattern for a keyword or phrase."""
    escaped = re.escape(keyword.lower())
    if re.fullmatch(r'[a-z]+(?: [a-z]+)*', keyword.lower()):
        # Alphabetic word/phrase: allow simple plural/verb suffixes on the
        # last word so "idea" matches "ideas", "invest" matches "investing".
        escaped += r"(?:s|es|ing|ed)?"
    # Lookarounds instead of \b so symbol keywords like "$" also work.
    return re.compile(r'(?<!\w)(?:' + escaped + r')(?!\w)')


class NoteCategorizer:
    """Categorize and organize notes by themes"""

    # Phone numbers / emails are near-certain contact notes.
    _PHONE_RE = re.compile(r'(?<!\d)(?:\+?\d[\d\s\-.]{8,14}\d)(?!\d)')
    _EMAIL_RE = re.compile(r'\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b', re.IGNORECASE)
    _URL_RE = re.compile(r'https?://\S+|\bwww\.\S+|\b\w+\.(?:com|net|org|io)\b',
                         re.IGNORECASE)
    _CODE_RE = re.compile(r'function\s*\(|def\s+\w+|class\s+\w+\s*[:({]|'
                          r'</?\w+>|\bimport\s+\w+|console\.log|=>')
    _CURRENCY_RE = re.compile(r'[$₦€£]\s?\d|\d\s?(?:usd|ngn|eur|gbp|naira|dollars?)\b',
                              re.IGNORECASE)

    def __init__(self):
        self.categories = {
            'Business Ideas': [
                'business', 'startup', 'company', 'revenue', 'profit', 'market', 'customer',
                'product', 'service', 'venture', 'funding', 'monetize', 'scale',
                'opportunity', 'competitor', 'strategy', 'launch', 'pitch', 'entrepreneur',
                'marketing', 'seo', 'content marketing', 'branding', 'positioning',
                'business idea', 'business plan'
            ],
            'Financial/Money': [
                'money', 'cash', 'payment', 'debt', 'loan', 'budget', 'expense', 'income',
                'salary', 'cost', 'price', 'financial', 'bank', 'account', 'investment',
                'invest', 'portfolio', 'savings', 'naira', 'dollar', 'pay',
                'mortgage', 'insurance', 'tax', 'crypto', 'bitcoin', 'trading', 'rent'
            ],
            'Personal Goals': [
                'goal', 'achieve', 'target', 'objective', 'dream', 'aspiration',
                'improve', 'habit', 'routine', 'personal growth', 'growth',
                'development', 'resolution', 'milestone', 'progress', 'therapy',
                'new year resolution'
            ],
            'Work/Career': [
                'work', 'job', 'career', 'office', 'meeting', 'project', 'deadline',
                'boss', 'colleague', 'client', 'resume', 'interview', 'promotion',
                'performance', 'team', 'department', 'professional', 'upwork', 'freelance'
            ],
            'Technology/Development': [
                'code', 'coding', 'programming', 'software', 'app', 'website', 'development',
                'tech', 'computer', 'system', 'database', 'api', 'framework', 'algorithm',
                'python', 'javascript', 'html', 'css', 'server', 'cloud', 'github', 'bug',
                'deploy'
            ],
            'Health/Fitness': [
                'health', 'fitness', 'exercise', 'workout', 'diet', 'nutrition', 'gym',
                'weight', 'doctor', 'medicine', 'wellness', 'mental health', 'stress',
                'sleep', 'meditation', 'hospital', 'appointment'
            ],
            'Contacts/People': [
                'contact', 'phone', 'email', 'address', 'friend', 'family',
                'partner', 'relationship', 'network', 'connection', 'birthday'
            ],
            'Travel/Places': [
                'travel', 'trip', 'vacation', 'flight', 'hotel', 'country', 'city',
                'visit', 'destination', 'location', 'place', 'journey',
                'passport', 'visa', 'booking', 'airport'
            ],
            'Shopping/Items': [
                'buy', 'purchase', 'shopping', 'store', 'item', 'brand',
                'order', 'delivery', 'discount', 'sale', 'amazon', 'grocery',
                'groceries', 'shopping list'
            ],
            'Ideas/Thoughts': [
                'idea', 'thought', 'concept', 'inspiration', 'brainstorm', 'creative',
                'innovation', 'solution', 'approach', 'method'
            ],
            'Tasks/Reminders': [
                'todo', 'task', 'reminder', 'remember', 'call', 'check',
                'follow up', 'schedule', 'appointment', 'urgent', 'important',
                'deadline', 'to do', 'dont forget', "don't forget"
            ],
            'Education/Learning': [
                'learn', 'study', 'course', 'book', 'education', 'knowledge', 'skill',
                'training', 'certification', 'degree', 'school', 'university', 'research',
                'tutorial', 'lesson'
            ]
        }

    def _score(self, content_lower: str, keywords: List[str]) -> int:
        """Score content against a keyword list. Phrases count double."""
        score = 0
        for keyword in keywords:
            if _keyword_pattern(keyword).search(content_lower):
                score += 2 if ' ' in keyword else 1
        return score

    def categorize_note(self, content: str) -> str:
        """Categorize a single note based on its content"""
        if not content:
            return 'Miscellaneous'

        content_lower = content.lower()

        # Contact details are a near-certain signal - decide immediately.
        if self._PHONE_RE.search(content) or self._EMAIL_RE.search(content):
            return 'Contacts/People'

        scores = {category: self._score(content_lower, keywords)
                  for category, keywords in self.categories.items()}

        # Strong signals boost their category instead of overriding others,
        # so "startup revenue $2M pitch deck" stays a business note.
        if self._CURRENCY_RE.search(content):
            scores['Financial/Money'] = scores.get('Financial/Money', 0) + 2
        if self._CODE_RE.search(content):
            scores['Technology/Development'] = scores.get('Technology/Development', 0) + 3
        elif self._URL_RE.search(content):
            scores['Technology/Development'] = scores.get('Technology/Development', 0) + 1

        best_category = max(scores, key=lambda c: scores[c])
        return best_category if scores[best_category] > 0 else 'Miscellaneous'

    def categorize_notes(self, notes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize all notes and return grouped by category"""
        categorized = defaultdict(list)

        for note in notes:
            category = self.categorize_note(note['content'])
            note['category'] = category
            categorized[category].append(note)

        return dict(categorized)

    def get_category_summary(self, categorized_notes: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
        """Get summary of notes count per category"""
        return {category: len(notes) for category, notes in categorized_notes.items()}

    def add_custom_category(self, name: str, keywords: List[str]):
        """Add a custom category with keywords"""
        self.categories[name] = keywords

    def get_categories(self) -> Dict[str, List[str]]:
        """Get all available categories and their keywords"""
        return self.categories.copy()
