#!/usr/bin/env python3
"""Generate comprehensive programming references for all languages"""
from pathlib import Path

# Comprehensive resources for each language
REFERENCES = {
    'python': {
        'official': [
            'https://docs.python.org/3/',
            'https://peps.python.org/',
            'https://devguide.python.org/',
            'https://pypi.org/',
        ],
        'tutorials': [
            'https://realpython.com/',
            'https://www.w3schools.com/python/',
            'https://www.codecademy.com/learn/learn-python-3',
            'https://www.learnpython.org/',
            'https://pythonbasics.org/',
        ],
        'libraries': [
            'https://numpy.org/doc/',
            'https://pandas.pydata.org/docs/',
            'https://fastapi.tiangolo.com/',
            'https://docs.djangoproject.com/',
            'https://flask.palletsprojects.com/',
            'https://requests.readthedocs.io/',
            'https://www.crummy.com/software/BeautifulSoup/',
        ],
        'best_practices': [
            'https://github.com/treyhunner/pep8',
            'https://docs.python-guide.org/',
            'https://refactoring.guru/design-patterns/python',
            'https://realpython.com/python-code-quality/',
            'https://realpython.com/python-testing/',
        ],
        'algorithms': [
            'https://github.com/TheAlgorithms/Python',
            'https://www.geeksforgeeks.org/python-programming-language/',
            'https://leetcode.com/problemset/all/',
            'https://www.hackerrank.com/domains/python',
        ],
    },
    'javascript': {
        'official': [
            'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
            'https://tc39.es/ecma262/',
            'https://nodejs.org/en/docs/',
            'https://www.w3schools.com/js/',
        ],
        'frameworks': [
            'https://react.dev/',
            'https://vuejs.org/',
            'https://angular.io/',
            'https://svelte.dev/',
            'https://nextjs.org/docs',
        ],
        'best_practices': [
            'https://github.com/airbnb/javascript',
            'https://javascript.info/',
            'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
        ],
        'testing': [
            'https://jestjs.io/',
            'https://vitest.dev/',
            'https://www.cypress.io/',
            'https://mochajs.org/',
        ],
    },
    'rust': {
        'official': [
            'https://www.rust-lang.org/learn',
            'https://doc.rust-lang.org/book/',
            'https://doc.rust-lang.org/rust-by-example/',
            'https://crates.io/',
            'https://docs.rs/',
        ],
        'learning': [
            'https://rustlings.crab/',
            'https://exercism.org/tracks/rust',
            'https://www.rust-lang.org/what/cli',
            'https://github.com/rust-lang/rustlings',
        ],
        'web': [
            'https://actix.rs/',
            'https://rocket.rs/',
            'https://tokio.rs/',
            'https://github.com/SergioBenitez/Rocket',
        ],
    },
    'go': {
        'official': [
            'https://go.dev/doc/',
            'https://go.dev/learn/',
            'https://pkg.go.dev/',
            'https://github.com/golang/go',
        ],
        'tutorials': [
            'https://gobyexample.com/',
            'https://www.w3schools.com/go/',
            'https://exercism.org/tracks/go',
            'https://go.dev/tour/',
        ],
        'web': [
            'https://gin-gonic.com/',
            'https://gofiber.io/',
            'https://echo.labstack.com/',
            'https://github.com/gin-gonic/gin',
        ],
    },
}

# Add more languages with basic references
for lang in ['java', 'cpp', 'csharp', 'ruby', 'php', 'swift', 'kotlin', 'typescript', 'sql', 'bash']:
    REFERENCES[lang] = {
        'official': [f'https://{lang}.org/docs/', f'https://en.cppreference.com/w/{lang}'],
        'tutorials': [f'https://www.w3schools.com/{lang}/', f'https://exercism.org/tracks/{lang}'],
        'best_practices': [f'https://github.com/search?q={lang}+best+practices'],
    }

for lang in REFERENCES:
    lang_dir = Path(lang)
    lang_dir.mkdir(exist_ok=True)
    
    with open(lang_dir / f"{lang}_references.md", 'w') as f:
        f.write(f"# {lang.upper()} Programming Resources\n\n")
        
        for category, urls in REFERENCES[lang].items():
            f.write(f"## {category.replace('_', ' ').title()}\n")
            for url in urls:
                f.write(f"{url}\n")
            f.write("\n")
    
    print(f"✅ Generated {lang}_references.md")

print("\n🎉 All reference files generated!")
