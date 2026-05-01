import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\drawclaw"
files = {}

files["critique/bad_examples/bad_examples.md"] = """# Bad Examples - Learning from Failure

## Why Study Bad Art
Studying failure is the fastest path to improvement. Professionals study bad art more than good art because it teaches what NOT to do.

## Common Failure Categories
| Category | What Goes Wrong | How to Spot It |
|----------|----------------|----------------|
| Tangent Lines | Lines that touch but do not overlap | Objects appear to merge |
| Laddered Perspective | Inconsistent vanishing points | Scene looks distorted |
| Symbolic Drawing | Drawing what you know, not what you see | Cartoon-like despite realism attempt |
| Flat Rendering | No value range | No depth, formless |
| Stiff Poses | No line of action | Figure looks like a statue |
| Floating Objects | No cast shadows | Objects appear disconnected |

## Resources
| Resource | URL |
|----------|-----|
| Proko Critiques | https://www.youtube.com/playlist?list=PLtG4P3lq8RHFBeVaruf2JjyQmZJH4__ZG |
| Istebrak Critique Hours | https://www.youtube.com/@Istebrak/playlists |
| Sinix Design - Why Your Art Sucks | https://www.youtube.com/watch?v=ZQ6TffKbiGQ |
| r/ArtCrit | https://www.reddit.com/r/ArtCrit/ |
"""

files["critique/before_after_critiques/before_after_critiques.md"] = """# Before/After Critiques

## Paintover Examples
| Resource | URL |
|----------|-----|
| Sinix Design Paintover Pals | https://www.youtube.com/@SinixDesign |
| Marc Brunet Paintovers | https://www.youtube.com/@YTartschool |
| Trent Kaniuga Critique Series | https://www.youtube.com/@TrentKaniuga |
| Mohammed Agbadi Critiques | https://www.youtube.com/@mohammedagbadi |

## Self-Critique Method
| Step | Action |
|------|--------|
| 1 | Flip canvas horizontally - reveals hidden errors |
| 2 | View as thumbnail - shows composition problems |
| 3 | Convert to grayscale - reveals value issues |
| 4 | Overlay reference - shows proportional errors |
| 5 | Rest the image for 24 hours - reveals new problems |
| 6 | Compare to master work - reveals skill gaps |
"""

files["production/art_director_feedback/art_director_feedback.md"] = """# Art Director Feedback Standards

## How Art Directors Evaluate Work
1. Does it solve the brief?
2. Does it communicate clearly?
3. Is the craftsmanship at professional level?
4. Would I put this in front of a client?

## Common AD Feedback
| Feedback | Real Meaning |
|----------|-------------|
| Push the design | Make it more extreme, less safe |
| It needs more love | Polish and detail are insufficient |
| The read is unclear | Silhouette/values don\'t communicate |
| Too noisy | Too many competing focal points |
| It feels flat | No depth or atmosphere |
| Explore more options | You settled too early |
| Check your values | Contrast is weak |

## Resources
| Resource | URL |
|----------|-----|
| How to Take Art Direction | https://www.creativebloq.com/career/art-director-feedback |
| Art Direction for Games | https://www.artstation.com/learning/courses/ |
"""

files["production/portfolio_review/portfolio_review.md"] = """# Portfolio Review Standards

## What Professionals Look For
| Criterion | What It Means |
|-----------|---------------|
| Consistency | Same quality across all pieces |
| Fundamentals | Strong drawing, values, color, composition |
| Design Thinking | Not just copying - original design decisions |
| Range | Different subject matter, styles, techniques |
| Presentation | Clean photos/scans, organized layout |

## Portfolio Structure
| Section | Pieces | Purpose |
|---------|--------|---------|
| Hero Piece | 1-2 | Best work, first impression |
| Core Work | 5-8 | Demonstrates primary skills |
| Process Work | 2-3 | Shows thinking, sketches to final |
| Specialty | 2-3 | Unique strength area |

## Resources
| Resource | URL |
|----------|-----|
| ArtStation Learning | https://www.artstation.com/learning/courses/ |
| Lightbox Expo Reviews | https://www.lightboxexpo.com/ |
"""

files["mental_models/decision_making/decision_making.md"] = """# Artistic Decision Making

## The Senior Artist Framework
Senior artists think: what problem am I solving?

## Decision Hierarchy
| Priority | Question |
|----------|----------|
| 1 | What emotional response do I want? |
| 2 | What is the focal point? |
| 3 | What mood serves the story? |
| 4 | What lighting supports the mood? |
| 5 | What value structure creates focus? |
| 6 | What color scheme reinforces emotion? |
| 7 | What level of detail serves the piece? |

## When to Stop
- Have I communicated the idea?
- Do additions improve or distract?
- Would the audience understand it?
"""

files["mental_models/artistic_judgment/artistic_judgment.md"] = """# Artistic Judgment and Taste

## The Taste Gap
Taste develops before skill. This gap causes frustration but drives improvement.

| Stage | Gap |
|-------|-----|
| Beginner | No gap (can\'t see errors yet) |
| Intermediate | Maximum gap (sees errors, can\'t fix them) |
| Advanced | Narrowing gap |
| Expert | Gap still exists, embraced |

## Judgment Questions
Before: Why am I making this?
During: What matters most right now?
After: Does this achieve the goal?
Next day: What would I change?

## References
| Resource | URL |
|----------|-----|
| James Gurney | https://www.gurneyjourney.com/ |
| Muddy Colors | https://www.muddycolors.com/ |
| Art Renewal Center | https://www.artrenewal.org/ |
"""

files["mental_models/design_tradeoffs/design_tradeoffs.md"] = """# Design Tradeoffs

## Common Tradeoffs
| Tradeoff | Choice A | Choice B |
|----------|----------|----------|
| Realism vs Expression | Accurate anatomy | Emotional impact |
| Detail vs Read | Intricate rendering | Clear silhouette |
| Speed vs Quality | Meet deadline | Perfect piece |
| Safety vs Innovation | Proven approach | Experimental risk |

## Decision Framework
1. Identify non-negotiables
2. List what can be traded
3. Decide what serves the primary goal
4. Commit and execute

Every creative decision is a tradeoff. The skill is knowing what to sacrifice.
"""

files["mental_models/visual_problem_solving/visual_problem_solving.md"] = """# Visual Problem Solving

## The Problem-Solving Loop
1. OBSERVE - What is actually wrong?
2. ANALYZE - What is the root cause?
3. REFERENCE - How have professionals solved this?
4. ITERATE - Try 3 quick solutions
5. EVALUATE - Which works best?
6. REFINE - Polish

## Common Root Causes
| Symptom | Root Cause |
|---------|-----------|
| Drawing looks flat | No value structure |
| Character looks stiff | No gesture/line of action |
| Composition feels off | No clear focal point |
| Colors look muddy | Poor value separation |
| Design looks boring | Too safe, no exaggeration |

## Resources
| Resource | URL |
|----------|-----|
| Feng Zhu Design Cinema | https://www.youtube.com/@FZDSCHOOL |
| Proko Draftsmen Podcast | https://www.youtube.com/@Draftsmen |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\\nDone! Created {len(files)} files.")
