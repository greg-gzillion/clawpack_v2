import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\drawclaw"

files = {}

files["drawing_exercises/drawing_exercises.md"] = """# Drawing Exercises Reference

## Warm-Up Exercises
| Exercise | URL |
|----------|-----|
| Blind Contour Drawing | https://www.artistsnetwork.com/art-mediums/drawing/blind-contour-drawing/ |
| Gesture Drawing Practice | https://www.artistsnetwork.com/art-mediums/drawing/gesture-drawing/ |
| 30 Second Sketches | https://line-of-action.com/ |
| Continuous Line Drawing | https://www.studentartguide.com/articles/line-drawing |
| Non-Dominant Hand Drawing | https://www.creativebloq.com/art/drawing-exercises-912763 |

## Form & Structure
| Exercise | URL |
|----------|-----|
| Draw a Box Challenge | https://drawabox.com/ |
| Sphere Shading | https://www.artistsnetwork.com/art-mediums/drawing/how-to-draw-a-sphere/ |
| Cube in Perspective | https://www.artistsnetwork.com/art-techniques/perspective-drawing/ |
| Cylinder Practice | https://www.artistsnetwork.com/art-mediums/drawing/basic-forms/ |
| Cross-Contour Drawing | https://www.artistsnetwork.com/art-mediums/drawing/cross-contour-drawing/ |

## Observation Skills
| Exercise | URL |
|----------|-----|
| Negative Space Drawing | https://www.artistsnetwork.com/art-mediums/drawing/negative-space-drawing/ |
| Upside Down Drawing | https://www.artistsnetwork.com/art-techniques/right-brain-drawing/ |
| Value Studies | https://www.artistsnetwork.com/art-techniques/value-drawing/ |
| Texture Studies | https://www.artistsnetwork.com/art-mediums/drawing/texture-drawing/ |
| Master Studies | https://www.artistsnetwork.com/art-history/masters/ |

## Daily Practice
| Resource | URL |
|----------|-----|
| r/SketchDaily | https://www.reddit.com/r/SketchDaily/ |
| Quickposes | https://quickposes.com/ |
| Line of Action | https://line-of-action.com/ |
| SketchDaily Reference | https://www.sketchdaily.net/ |
"""

files["art_history/art_history.md"] = """# Art History Reference

## Prehistoric to Medieval
| Period | URL |
|--------|-----|
| Cave Paintings | https://www.metmuseum.org/toah/hd/lasc/hd_lasc.htm |
| Egyptian Art | https://www.metmuseum.org/toah/hd/egyp/hd_egyp.htm |
| Greek Art | https://www.metmuseum.org/toah/hd/grmo/hd_grmo.htm |
| Roman Art | https://www.metmuseum.org/toah/hd/roem/hd_roem.htm |
| Byzantine Art | https://www.metmuseum.org/toah/hd/byza/hd_byza.htm |
| Medieval Art | https://www.metmuseum.org/toah/hd/medi/hd_medi.htm |

## Renaissance & Baroque
| Period | URL |
|--------|-----|
| Italian Renaissance | https://www.metmuseum.org/toah/hd/itar/hd_itar.htm |
| Northern Renaissance | https://www.metmuseum.org/toah/hd/nren/hd_nren.htm |
| High Renaissance | https://www.metmuseum.org/toah/hd/hire/hd_hire.htm |
| Baroque Art | https://www.metmuseum.org/toah/hd/baro/hd_baro.htm |
| Dutch Golden Age | https://www.metmuseum.org/toah/hd/dutc/hd_dutc.htm |
| Rococo | https://www.metmuseum.org/toah/hd/roco/hd_roco.htm |

## 19th Century
| Movement | URL |
|----------|-----|
| Neoclassicism | https://www.metmuseum.org/toah/hd/neoc_1/hd_neoc_1.htm |
| Romanticism | https://www.metmuseum.org/toah/hd/roma/hd_roma.htm |
| Realism | https://www.metmuseum.org/toah/hd/rlsm/hd_rlsm.htm |
| Impressionism | https://www.metmuseum.org/toah/hd/imml/hd_imml.htm |
| Post-Impressionism | https://www.metmuseum.org/toah/hd/poim/hd_poim.htm |
| Art Nouveau | https://www.metmuseum.org/toah/hd/artn/hd_artn.htm |

## 20th-21st Century
| Movement | URL |
|----------|-----|
| Cubism | https://www.tate.org.uk/art/art-terms/c/cubism |
| Surrealism | https://www.tate.org.uk/art/art-terms/s/surrealism |
| Abstract Expressionism | https://www.moma.org/collection/terms/abstract-expressionism |
| Pop Art | https://www.tate.org.uk/art/art-terms/p/pop-art |
| Minimalism | https://www.moma.org/collection/terms/minimalism |
| Contemporary Art | https://www.moma.org/collection/ |

## Asian Art
| Period | URL |
|--------|-----|
| Chinese Painting | https://www.metmuseum.org/toah/hd/chin/hd_chin.htm |
| Japanese Woodblock | https://www.metmuseum.org/toah/hd/ukiy/hd_ukiy.htm |
| Korean Art | https://www.metmuseum.org/toah/hd/kart/hd_kart.htm |
| Indian Art | https://www.metmuseum.org/toah/hd/indt/hd_indt.htm |

## African & Indigenous Art
| Region | URL |
|--------|-----|
| African Art | https://www.metmuseum.org/toah/hd/afri/hd_afri.htm |
| Oceanic Art | https://www.metmuseum.org/toah/hd/ocea/hd_ocea.htm |
| Pre-Columbian Art | https://www.metmuseum.org/toah/hd/prec/hd_prec.htm |
| Native American Art | https://www.metmuseum.org/toah/hd/nasm/hd_nasm.htm |
"""

files["concept_design/concept_design.md"] = """# Concept Design Reference

## Character Design
| Concept | URL |
|---------|-----|
| Character Design Process | https://www.creativebloq.com/character-design/tips-5132677 |
| Silhouette Design | https://www.creativebloq.com/features/character-design-silhouettes |
| Character Turnarounds | https://www.artstation.com/learning/courses/aZJ/introduction-to-character-design/ |
| Costume Design | https://www.creativebloq.com/fashion/character-costume-design |
| Expression Sheets | https://www.creativebloq.com/character-design/expression-sheets-11121192 |

## Creature Design
| Concept | URL |
|---------|-----|
| Creature Anatomy | https://www.creativebloq.com/3d/creature-design-tips-101292 |
| Monster Design | https://www.artstation.com/learning/courses/ |
| Hybrid Creatures | https://www.creativebloq.com/illustration/creature-design-12121454 |

## World Building
| Concept | URL |
|---------|-----|
| World Building Guide | https://www.creativebloq.com/entertainment/world-building-guide |
| Map Making | https://www.fantasticmaps.com/ |
| Environment Concept Art | https://www.creativebloq.com/career/concept-artist-11121137 |

## Prop Design
| Concept | URL |
|---------|-----|
| Prop Design Tutorial | https://www.artstation.com/learning/courses/ |
| Weapon Design | https://www.creativebloq.com/digital-art/weapon-design-tips |
| Vehicle Design | https://www.creativebloq.com/illustration/vehicle-design |

## Visual Development
| Concept | URL |
|---------|-----|
| VisDev Process | https://www.creativebloq.com/animation/visual-development-11121137 |
| Color Scripts | https://www.artofthetitle.com/ |
| Style Guides | https://www.artstation.com/channels/visual_development |
"""

files["illustration/illustration.md"] = """# Illustration Reference

## Book Illustration
| Concept | URL |
|---------|-----|
| Children's Book Illustration | https://www.creativebloq.com/illustration/childrens-book-illustration |
| Editorial Illustration | https://www.creativebloq.com/illustration/editorial-illustration |
| Cover Art | https://www.creativebloq.com/illustration/book-cover-design |
| Scientific Illustration | https://www.gnsi.org/ |

## Commercial Illustration
| Concept | URL |
|---------|-----|
| Advertising Illustration | https://www.creativebloq.com/illustration/advertising |
| Product Illustration | https://www.creativebloq.com/illustration/product-illustration |
| Fashion Illustration | https://www.creativebloq.com/fashion/fashion-illustration |
| Food Illustration | https://www.creativebloq.com/illustration/food-illustration |

## Narrative Art
| Concept | URL |
|---------|-----|
| Storytelling Through Art | https://www.creativebloq.com/illustration/narrative-art |
| Sequential Art | https://www.creativebloq.com/comics/ |
| Visual Storytelling | https://www.artofthetitle.com/ |
| Picture Book Design | https://www.creativebloq.com/illustration/picture-books |

## Styles & Approaches
| Style | URL |
|-------|-----|
| Vector Illustration | https://www.creativebloq.com/digital-art/vector-art |
| Mixed Media Illustration | https://www.creativebloq.com/illustration/mixed-media |
| Digital Illustration | https://www.creativebloq.com/digital-art/digital-illustration |
| Traditional Illustration | https://www.creativebloq.com/illustration/traditional-illustration |
"""

files["character_design/character_design.md"] = """# Character Design Reference

## Fundamentals
| Concept | URL |
|---------|-----|
| Character Design Basics | https://www.creativebloq.com/character-design/tips-5132677 |
| Shape Language | https://www.creativebloq.com/features/character-design-shape-language |
| Color in Character Design | https://www.creativebloq.com/character-design/color-theory |
| Proportions Guide | https://www.artistsnetwork.com/art-mediums/drawing/human-proportions/ |

## Archetypes
| Concept | URL |
|---------|-----|
| Character Archetypes | https://www.creativebloq.com/character-design/archetypes |
| Hero Design | https://www.creativebloq.com/character-design/hero-design |
| Villain Design | https://www.creativebloq.com/character-design/villain-design |
| Sidekick Design | https://www.creativebloq.com/character-design/sidekick-design |

## Expression & Pose
| Concept | URL |
|---------|-----|
| Facial Expressions | https://www.artistsnetwork.com/art-mediums/drawing/facial-expressions/ |
| Dynamic Poses | https://www.artistsnetwork.com/art-mediums/drawing/dynamic-poses/ |
| Gesture Language | https://www.creativebloq.com/character-design/body-language |
| Emotion Through Posture | https://www.artistsnetwork.com/art-techniques/gesture-drawing/ |

## Industry Standards
| Resource | URL |
|----------|-----|
| Model Sheets | https://www.creativebloq.com/character-design/model-sheets |
| Turnarounds | https://www.artstation.com/learning/courses/ |
| Expression Sheets | https://www.creativebloq.com/character-design/expression-sheets |
| Character Bible | https://www.creativebloq.com/character-design/character-bible |
"""

files["environment_design/environment_design.md"] = """# Environment Design Reference

## Fundamentals
| Concept | URL |
|---------|-----|
| Environment Design Process | https://www.creativebloq.com/career/concept-artist-11121137 |
| Composition for Environments | https://www.artistsnetwork.com/art-techniques/composition/ |
| Atmospheric Perspective | https://www.artistsnetwork.com/art-techniques/atmospheric-perspective/ |
| Lighting Environments | https://www.creativebloq.com/digital-art/lighting-environments |

## Natural Environments
| Environment | URL |
|------------|-----|
| Forest Design | https://www.creativebloq.com/digital-art/forest-concept-art |
| Mountain Landscapes | https://www.artistsnetwork.com/art-mediums/pastel/mountain-landscape/ |
| Ocean & Water | https://www.artistsnetwork.com/art-mediums/drawing/drawing-water/ |
| Desert Environments | https://www.creativebloq.com/digital-art/desert-concept-art |
| Snow & Ice | https://www.artistsnetwork.com/art-mediums/pastel/winter-landscape/ |

## Built Environments
| Environment | URL |
|------------|-----|
| City Design | https://www.creativebloq.com/digital-art/city-concept-art |
| Interior Design | https://www.creativebloq.com/interior-design |
| Architecture Drawing | https://www.artistsnetwork.com/art-mediums/drawing/architectural-drawing/ |
| Sci-Fi Environments | https://www.creativebloq.com/digital-art/sci-fi-concept-art |
| Fantasy Worlds | https://www.creativebloq.com/digital-art/fantasy-concept-art |

## Mood & Atmosphere
| Concept | URL |
|---------|-----|
| Creating Mood | https://www.artistsnetwork.com/art-techniques/creating-mood/ |
| Time of Day | https://www.creativebloq.com/digital-art/lighting-time-of-day |
| Weather Effects | https://www.artistsnetwork.com/art-mediums/pastel/weather-landscape/ |
| Color Scripts | https://www.artofthetitle.com/ |
"""

files["storyboarding/storyboarding.md"] = """# Storyboarding Reference

## Fundamentals
| Concept | URL |
|---------|-----|
| Storyboarding Basics | https://www.studiobinder.com/blog/what-is-a-storyboard/ |
| Shot Composition | https://www.studiobinder.com/blog/rules-of-shot-composition/ |
| Camera Angles | https://www.studiobinder.com/blog/types-of-camera-shot-angles/ |
| Visual Continuity | https://www.creativebloq.com/animation/storyboarding-tips |

## Cinematography
| Concept | URL |
|---------|-----|
| Camera Movement | https://www.studiobinder.com/blog/different-types-of-camera-movements/ |
| Framing Guide | https://www.studiobinder.com/blog/types-of-camera-framing/ |
| Lighting for Film | https://www.studiobinder.com/blog/film-lighting-techniques/ |
| Lens Choices | https://www.studiobinder.com/blog/focal-length-camera-lenses/ |

## Sequential Art
| Concept | URL |
|---------|-----|
| Panel Layout | https://www.creativebloq.com/comics/panel-layout |
| Pacing | https://www.creativebloq.com/animation/storyboarding-pacing |
| Transitions | https://www.studiobinder.com/blog/types-of-editing-transitions/ |
| Thumbnail Process | https://www.creativebloq.com/animation/storyboard-thumbnails |

## Professional Practice
| Resource | URL |
|----------|-----|
| Storyboard Pro Guide | https://www.toonboom.com/products/storyboard-pro |
| Animatic Creation | https://www.creativebloq.com/animation/animatic |
| Studio Workflows | https://www.artstation.com/learning/courses/ |
| Portfolio Examples | https://www.storyboardart.org/ |
"""

files["animation/animation.md"] = """# Animation Reference

## Principles
| Principle | URL |
|-----------|-----|
| 12 Principles of Animation | https://www.creativebloq.com/advice/understand-the-12-principles-of-animation |
| Squash & Stretch | https://www.animatorisland.com/ |
| Timing & Spacing | https://www.animationmentor.com/ |
| Anticipation | https://www.creativebloq.com/animation/animation-tips |

## 2D Animation
| Concept | URL |
|---------|-----|
| Frame by Frame | https://www.creativebloq.com/animation/2d-animation |
| Keyframe Animation | https://www.animationmentor.com/blog/ |
| In-Betweening | https://www.creativebloq.com/animation/inbetweening |
| Walk Cycles | https://www.animatorisland.com/how-to-animate-a-walk-cycle/ |

## 3D Animation
| Concept | URL |
|---------|-----|
| Rigging Basics | https://www.creativebloq.com/3d/rigging |
| Motion Capture | https://www.creativebloq.com/animation/motion-capture |
| Physics Simulation | https://www.creativebloq.com/3d/animation-physics |

## Motion Graphics
| Concept | URL |
|---------|-----|
| Motion Design | https://www.creativebloq.com/motion-graphics |
| Kinetic Typography | https://www.creativebloq.com/typography/kinetic-typography |
| UI Animation | https://www.creativebloq.com/ui-design/animation |
| Logo Animation | https://www.creativebloq.com/animation/logo-animation |
"""

files["typography/typography.md"] = """# Typography Reference

## Fundamentals
| Concept | URL |
|---------|-----|
| Typography Basics | https://www.creativebloq.com/typography/what-is-typography |
| Font vs Typeface | https://www.creativebloq.com/features/typography-terms |
| Type Anatomy | https://www.creativebloq.com/typography/type-anatomy |
| Kerning & Tracking | https://www.creativebloq.com/typography/kerning-tracking |

## Classification
| Type | URL |
|------|-----|
| Serif Fonts | https://www.creativebloq.com/typography/serif-fonts |
| Sans Serif | https://www.creativebloq.com/typography/sans-serif-fonts |
| Script Fonts | https://www.creativebloq.com/typography/script-fonts |
| Display Fonts | https://www.creativebloq.com/typography/display-fonts |
| Monospace | https://www.creativebloq.com/typography/monospaced-fonts |

## Design
| Concept | URL |
|---------|-----|
| Font Pairing | https://www.creativebloq.com/typography/font-pairing |
| Hierarchy | https://www.creativebloq.com/typography/typographic-hierarchy |
| Readability | https://www.creativebloq.com/typography/readability |
| Responsive Type | https://www.creativebloq.com/typography/responsive-typography |

## Resources
| Resource | URL |
|----------|-----|
| Google Fonts | https://fonts.google.com/ |
| Adobe Fonts | https://fonts.adobe.com/ |
| Font Squirrel | https://www.fontsquirrel.com/ |
| WhatTheFont | https://www.myfonts.com/pages/whatthefont |
"""

files["graphic_design/graphic_design.md"] = """# Graphic Design Reference

## Fundamentals
| Concept | URL |
|---------|-----|
| Design Principles | https://www.creativebloq.com/graphic-design/graphic-design-principles |
| Visual Hierarchy | https://www.creativebloq.com/graphic-design/visual-hierarchy |
| Grid Systems | https://www.creativebloq.com/graphic-design/grid-systems |
| White Space | https://www.creativebloq.com/graphic-design/white-space |

## Layout
| Concept | URL |
|---------|-----|
| Page Layout | https://www.creativebloq.com/graphic-design/page-layout |
| Magazine Design | https://www.creativebloq.com/graphic-design/magazine-design |
| Poster Design | https://www.creativebloq.com/graphic-design/poster-design |
| Book Design | https://www.creativebloq.com/graphic-design/book-design |

## Branding
| Concept | URL |
|---------|-----|
| Logo Design | https://www.creativebloq.com/graphic-design/logo-design |
| Brand Identity | https://www.creativebloq.com/graphic-design/brand-identity |
| Style Guides | https://www.creativebloq.com/graphic-design/style-guides |
| Packaging Design | https://www.creativebloq.com/graphic-design/packaging-design |

## UI/UX Design
| Concept | URL |
|---------|-----|
| UI Design Principles | https://www.creativebloq.com/ui-design |
| UX Design Process | https://www.creativebloq.com/ux-design |
| Wireframing | https://www.creativebloq.com/ux-design/wireframing |
| Prototyping | https://www.creativebloq.com/ux-design/prototyping |

## Tools
| Tool | URL |
|------|-----|
| Figma | https://www.figma.com/ |
| Adobe Illustrator | https://www.adobe.com/illustrator |
| Canva | https://www.canva.com/ |
| Inkscape | https://inkscape.org/ |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} reference files.")
