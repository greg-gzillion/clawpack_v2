python -c "
import os
base = r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\drawclaw'

files = {}

files['composition/composition.md'] = '''# Composition Reference

## Rule of Thirds
| Concept | URL |
|---------|-----|
| Rule of Thirds Explained | https://www.adobe.com/creativecloud/photography/discover/rule-of-thirds.html |
| Composition Techniques | https://photographylife.com/composition-in-photography |
| Golden Ratio in Art | https://www.creativebloq.com/design/designers-guide-golden-ratio-12121546 |
| Dynamic Symmetry | https://www.artistsnetwork.com/art-techniques/composition-dynamic-symmetry/ |
| Visual Balance | https://www.artistsnetwork.com/art-techniques/balance-in-art/ |

## Leading Lines & Flow
| Concept | URL |
|---------|-----|
| Leading Lines Guide | https://expertphotography.com/how-to-use-leading-lines/ |
| Diagonal Composition | https://www.picturecorrect.com/how-to-use-diagonal-lines-in-photography-composition/ |
| S-Curves and Flow | https://www.artistsnetwork.com/art-techniques/composition-flow/ |
| Eye Movement in Art | https://www.creativebloq.com/art/composition-tips-11121180 |

## Framing & Depth
| Concept | URL |
|---------|-----|
| Framing in Art | https://drawpaintacademy.com/framing/ |
| Creating Depth | https://www.artistsnetwork.com/art-techniques/create-depth-in-your-art/ |
| Foreground Middle Ground Background | https://www.artistsnetwork.com/art-mediums/pastel/foreground-middle-ground-background/ |
| Atmospheric Perspective | https://www.artistsnetwork.com/art-techniques/atmospheric-perspective/ |

## Advanced Composition
| Concept | URL |
|---------|-----|
| Composition in Landscape | https://www.artistsnetwork.com/art-mediums/pastel/landscape-composition/ |
| Portrait Composition | https://www.artistsnetwork.com/art-mediums/drawing/portrait-composition/ |
| Abstract Composition | https://www.moma.org/collection/terms/abstract-expressionism |
| Negative Space Design | https://www.creativebloq.com/graphic-design/negative-space |
'''

files['color_theory/color_theory.md'] = '''# Color Theory Reference

## Color Harmonies
| Concept | URL |
|---------|-----|
| Color Theory Basics | https://www.colormatters.com/color-and-design/basic-color-theory |
| Color Harmonies Guide | https://www.canva.com/colors/color-wheel/ |
| Adobe Color Wheel | https://color.adobe.com/create/color-wheel |
| Complementary Colors | https://www.artistsnetwork.com/art-techniques/color-mixing/complementary-colors/ |
| Analogous Colors | https://www.artistsnetwork.com/art-techniques/color-mixing/analogous-colors/ |

## Color Psychology
| Concept | URL |
|---------|-----|
| Color Meanings | https://www.color-meanings.com/ |
| Color in Art | https://www.artistsnetwork.com/art-techniques/color-mixing/color-theory/ |
| Warm vs Cool Colors | https://drawpaintacademy.com/warm-and-cool-colors/ |
| Emotional Color | https://www.creativebloq.com/colour/colour-emotion-11141367 |

## Advanced Color
| Concept | URL |
|---------|-----|
| Color Relativity | https://www.gurneyjourney.com/ |
| Light and Color | https://www.jamesgurney.com/ |
| Pigment vs Light | https://www.huevaluechroma.com/ |
| Munsell Color System | https://munsell.com/about-munsell-color/ |
| Color Mixing Guide | https://www.artistsnetwork.com/art-techniques/color-mixing/color-mixing-guide/ |

## Palettes & Schemes
| Concept | URL |
|---------|-----|
| Color Palette Generator | https://coolors.co/ |
| Color Scheme Designer | https://paletton.com/ |
| Gradients | https://uigradients.com/ |
| Material Design Colors | https://material.io/design/color |
'''

files['perspective/perspective.md'] = '''# Perspective Reference

## Linear Perspective
| Concept | URL |
|---------|-----|
| One Point Perspective | https://www.studentartguide.com/articles/one-point-perspective-drawing |
| Two Point Perspective | https://www.studentartguide.com/articles/two-point-perspective-drawing |
| Three Point Perspective | https://www.artistsnetwork.com/art-mediums/drawing/three-point-perspective/ |
| Multi-Point Perspective | https://www.artistsnetwork.com/art-techniques/perspective-drawing/ |

## Atmospheric Perspective
| Concept | URL |
|---------|-----|
| Aerial Perspective Guide | https://www.artistsnetwork.com/art-techniques/atmospheric-perspective/ |
| Creating Depth with Color | https://drawpaintacademy.com/aerial-perspective/ |
| Value and Distance | https://www.artistsnetwork.com/art-techniques/value-drawing/ |

## Specialized Perspective
| Concept | URL |
|---------|-----|
| Foreshortening | https://www.artistsnetwork.com/art-mediums/drawing/foreshortening/ |
| Curvilinear Perspective | https://www.artistsnetwork.com/art-techniques/curvilinear-perspective/ |
| Isometric Drawing | https://www.creativebloq.com/digital-art/isometric-drawing |
| Fish-Eye Perspective | https://www.artistsnetwork.com/art-techniques/fisheye-perspective/ |

## Architecture
| Concept | URL |
|---------|-----|
| Architectural Drawing | https://www.artistsnetwork.com/art-mediums/drawing/architectural-drawing/ |
| Interior Perspective | https://www.artistsnetwork.com/art-mediums/drawing/interior-drawing/ |
| Urban Sketching | https://urbansketchers.org/ |
'''

files['anatomy/anatomy.md'] = '''# Anatomy Reference

## Human Anatomy
| Concept | URL |
|---------|-----|
| Figure Drawing Basics | https://www.artistsnetwork.com/art-mediums/drawing/figure-drawing/ |
| Proportions Guide | https://www.artistsnetwork.com/art-mediums/drawing/human-proportions/ |
| Skeletal Structure | https://www.artistsnetwork.com/art-mediums/drawing/skeletal-structure/ |
| Muscular Anatomy | https://www.artistsnetwork.com/art-mediums/drawing/muscular-anatomy/ |

## Head & Face
| Concept | URL |
|---------|-----|
| Drawing Faces | https://rapidfireart.com/2015/12/07/how-to-draw-a-face-in-8-steps/ |
| Facial Proportions | https://www.artistsnetwork.com/art-mediums/drawing/facial-proportions/ |
| Drawing Eyes | https://www.artistsnetwork.com/art-mediums/drawing/drawing-eyes/ |
| Facial Expressions | https://www.artistsnetwork.com/art-mediums/drawing/facial-expressions/ |

## Hands & Feet
| Concept | URL |
|---------|-----|
| Drawing Hands | https://www.artistsnetwork.com/art-mediums/drawing/drawing-hands/ |
| Drawing Feet | https://www.artistsnetwork.com/art-mediums/drawing/drawing-feet/ |
| Hand Anatomy | https://www.creativebloq.com/art/how-draw-hands |

## Animal Anatomy
| Concept | URL |
|---------|-----|
| Animal Drawing Guide | https://www.artistsnetwork.com/art-mediums/drawing/animal-drawing/ |
| Bird Anatomy | https://www.thegnomonworkshop.com/tutorials/animal-anatomy |
| Horse Anatomy | https://www.artistsnetwork.com/art-mediums/drawing/horse-drawing/ |
| Cat & Dog Anatomy | https://www.creativebloq.com/art/how-draw-animals |

## Dynamic Figures
| Concept | URL |
|---------|-----|
| Gesture Drawing | https://www.artistsnetwork.com/art-mediums/drawing/gesture-drawing/ |
| Dynamic Poses | https://www.artistsnetwork.com/art-mediums/drawing/dynamic-poses/ |
| Action Lines | https://www.creativebloq.com/character-design/dynamic-poses |
'''

files['lighting/lighting.md'] = '''# Lighting Reference

## Light Types
| Concept | URL |
|---------|-----|
| Chiaroscuro Technique | https://www.artistsnetwork.com/art-history/chiaroscuro/ |
| Rembrandt Lighting | https://www.rembrandtlighting.com/ |
| Three Point Lighting | https://www.studiobinder.com/blog/3-point-lighting/ |
| Natural Light Guide | https://www.artistsnetwork.com/art-techniques/natural-light/ |
| Dramatic Lighting | https://www.creativebloq.com/art/dramatic-lighting |

## Shadows
| Concept | URL |
|---------|-----|
| Drawing Shadows | https://www.artistsnetwork.com/art-mediums/drawing/drawing-shadows/ |
| Core and Cast Shadows | https://drawpaintacademy.com/light-and-shadow/ |
| Shadow Colors | https://www.artistsnetwork.com/art-techniques/color-of-shadows/ |
| Ambient Occlusion | https://www.creativebloq.com/3d/ambient-occlusion |

## Light Effects
| Concept | URL |
|---------|-----|
| Golden Hour Guide | https://www.artistsnetwork.com/art-techniques/painting-golden-hour/ |
| Backlighting | https://www.creativebloq.com/photography/backlighting |
| Rim Light | https://www.studiobinder.com/blog/rim-light/ |
| Subsurface Scattering | https://www.creativebloq.com/3d/subsurface-scattering |
| Volumetric Lighting | https://www.creativebloq.com/3d/volumetric-lighting |

## Color of Light
| Concept | URL |
|---------|-----|
| Warm vs Cool Light | https://www.artistsnetwork.com/art-techniques/warm-cool-light/ |
| Colored Lighting | https://www.creativebloq.com/art/colored-lighting |
| Light Temperature | https://www.studiobinder.com/blog/color-temperature/ |
'''

files['art_styles/art_styles.md'] = '''# Art Styles Reference

## Classical & Traditional
| Style | URL |
|-------|-----|
| Realism | https://www.metmuseum.org/toah/hd/rlsm/hd_rlsm.htm |
| Impressionism | https://www.metmuseum.org/toah/hd/imml/hd_imml.htm |
| Post-Impressionism | https://www.metmuseum.org/toah/hd/poim/hd_poim.htm |
| Expressionism | https://www.tate.org.uk/art/art-terms/e/expressionism |
| Art Deco | https://www.vam.ac.uk/articles/art-deco |

## Modern
| Style | URL |
|-------|-----|
| Cubism | https://www.tate.org.uk/art/art-terms/c/cubism |
| Surrealism | https://www.tate.org.uk/art/art-terms/s/surrealism |
| Abstract Expressionism | https://www.moma.org/collection/terms/abstract-expressionism |
| Pop Art | https://www.tate.org.uk/art/art-terms/p/pop-art |
| Minimalism | https://www.moma.org/collection/terms/minimalism |

## Contemporary
| Style | URL |
|-------|-----|
| Digital Art | https://www.creativebloq.com/digital-art |
| Street Art | https://www.tate.org.uk/art/art-terms/s/street-art |
| Installation Art | https://www.tate.org.uk/art/art-terms/i/installation-art |
| Generative Art | https://www.artnome.com/news/2018/8/8/why-love-generative-art |
| Mixed Media | https://www.tate.org.uk/art/art-terms/m/mixed-media |

## Cultural Styles
| Style | URL |
|-------|-----|
| Ukiyo-e (Japanese) | https://www.metmuseum.org/toah/hd/ukiy/hd_ukiy.htm |
| Chinese Ink Painting | https://www.metmuseum.org/toah/hd/chin/hd_chin.htm |
| Aboriginal Art | https://www.aboriginalart.com.au/ |
| Islamic Art | https://www.metmuseum.org/toah/hd/figs/hd_figs.htm |
| African Mask Tradition | https://www.metmuseum.org/toah/hd/afrm/hd_afrm.htm |
'''

files['techniques/techniques.md'] = '''# Drawing Techniques Reference

## Line Work
| Technique | URL |
|-----------|-----|
| Contour Drawing | https://www.artistsnetwork.com/art-mediums/drawing/contour-drawing/ |
| Cross-Hatching | https://www.artistsnetwork.com/art-mediums/drawing/cross-hatching/ |
| Stippling | https://www.artistsnetwork.com/art-mediums/drawing/stippling/ |
| Gesture Drawing | https://www.artistsnetwork.com/art-mediums/drawing/gesture-drawing/ |
| Continuous Line | https://www.studentartguide.com/articles/line-drawing |

## Shading & Value
| Technique | URL |
|-----------|-----|
| Value Scale Guide | https://www.artistsnetwork.com/art-techniques/value-scale/ |
| Blending Techniques | https://www.artistsnetwork.com/art-mediums/drawing/blending/ |
| Scribbling Shade | https://www.artistsnetwork.com/art-mediums/drawing/scribbling/ |
| Circulism | https://www.artistsnetwork.com/art-mediums/drawing/circulism/ |
| Smooth Shading | https://www.artistsnetwork.com/art-mediums/drawing/smooth-shading/ |

## Painting Techniques
| Technique | URL |
|-----------|-----|
| Glazing | https://www.artistsnetwork.com/art-mediums/oil-painting/glazing/ |
| Impasto | https://www.moma.org/collection/terms/impasto |
| Dry Brush | https://www.artistsnetwork.com/art-mediums/oil-painting/dry-brush/ |
| Wet-on-Wet | https://www.artistsnetwork.com/art-mediums/oil-painting/wet-on-wet/ |
| Scumbling | https://www.artistsnetwork.com/art-mediums/oil-painting/scumbling/ |

## Advanced
| Technique | URL |
|-----------|-----|
| Grisaille | https://www.tate.org.uk/art/art-terms/g/grisaille |
| Sfumato | https://www.britannica.com/art/sfumato |
| Underpainting | https://www.artistsnetwork.com/art-techniques/underpainting/ |
| Alla Prima | https://www.artistsnetwork.com/art-techniques/alla-prima/ |
'''

files['famous_artists/famous_artists.md'] = '''# Famous Artists Reference

## Renaissance Masters
| Artist | URL |
|--------|-----|
| Leonardo da Vinci | https://www.leonardodavinci.net/ |
| Michelangelo | https://www.michelangelo.org/ |
| Raphael | https://www.raphaelsanzio.org/ |
| Caravaggio | https://www.caravaggio.org/ |
| Albrecht Durer | https://www.albrecht-durer.org/ |

## Impressionists
| Artist | URL |
|--------|-----|
| Claude Monet | https://www.claudemonetgallery.org/ |
| Pierre-Auguste Renoir | https://www.pierre-auguste-renoir.org/ |
| Edgar Degas | https://www.edgar-degas.org/ |
| Mary Cassatt | https://www.marycassatt.org/ |

## Post-Impressionists
| Artist | URL |
|--------|-----|
| Vincent van Gogh | https://www.vangoghgallery.com/ |
| Paul Cezanne | https://www.paulcezanne.org/ |
| Georges Seurat | https://www.georgesseurat.org/ |
| Paul Gauguin | https://www.paul-gauguin.net/ |

## Modern Masters
| Artist | URL |
|--------|-----|
| Pablo Picasso | https://www.pablopicasso.org/ |
| Salvador Dali | https://www.salvador-dali.org/ |
| Frida Kahlo | https://www.fridakahlo.org/ |
| Georgia O Keeffe | https://www.okeeffemuseum.org/ |
| M.C. Escher | https://mcescher.com/ |
| Edward Hopper | https://www.edwardhopper.net/ |

## Contemporary
| Artist | URL |
|--------|-----|
| David Hockney | https://www.hockney.com/ |
| Gerhard Richter | https://www.gerhard-richter.com/ |
| Yayoi Kusama | https://yayoikusamamuseum.jp/ |
| Banksy | https://www.banksy.co.uk/ |
| Kehinde Wiley | https://kehindewiley.com/ |
'''

files['digital_art/digital_art.md'] = '''# Digital Art Reference

## Software
| Tool | URL |
|------|-----|
| Procreate | https://procreate.com/ |
| Krita | https://krita.org/ |
| Clip Studio Paint | https://www.clipstudio.net/ |
| Photoshop | https://www.adobe.com/photoshop |
| Blender | https://www.blender.org/ |
| ZBrush | https://www.maxon.net/en/zbrush |

## Digital Painting
| Concept | URL |
|---------|-----|
| Digital Painting Basics | https://www.ctrlpaint.com/ |
| Layer Techniques | https://www.artistsnetwork.com/art-mediums/digital-art/layer-techniques/ |
| Brush Settings | https://www.creativebloq.com/digital-art/brush-guide |
| Color Grading | https://www.creativebloq.com/digital-art/color-grading |

## 3D Art
| Concept | URL |
|---------|-----|
| 3D Modeling Basics | https://www.creativebloq.com/3d/3d-modelling |
| Sculpting Guide | https://www.creativebloq.com/3d/digital-sculpting |
| Texturing | https://www.creativebloq.com/3d/texturing |
| Rendering | https://www.creativebloq.com/3d/rendering |

## Generative & AI Art
| Concept | URL |
|---------|-----|
| Processing | https://processing.org/ |
| p5.js | https://p5js.org/ |
| Generative Art Guide | https://www.artnome.com/news/2018/8/8/why-love-generative-art |
| Creative Coding | https://www.creativebloq.com/digital-art/creative-coding |

## Workflow
| Concept | URL |
|---------|-----|
| Digital Art Workflow | https://www.creativebloq.com/digital-art/digital-painting-workflow |
| File Management | https://www.creativebloq.com/digital-art/organizing-digital-art |
| Color Management | https://www.creativebloq.com/digital-art/color-management |
| Portfolio Building | https://www.artstation.com/ |
'''

files['traditional_media/traditional_media.md'] = '''# Traditional Media Reference

## Drawing Materials
| Medium | URL |
|--------|-----|
| Graphite Guide | https://www.artistsnetwork.com/art-mediums/drawing/graphite-drawing/ |
| Charcoal Drawing | https://www.artistsnetwork.com/art-mediums/drawing/charcoal-drawing/ |
| Colored Pencil | https://www.artistsnetwork.com/art-mediums/colored-pencil/ |
| Pastels | https://www.artistsnetwork.com/art-mediums/pastel/ |
| Pen & Ink | https://www.artistsnetwork.com/art-mediums/drawing/pen-and-ink/ |
| Markers | https://www.artistsnetwork.com/art-mediums/drawing/marker-drawing/ |

## Painting
| Medium | URL |
|--------|-----|
| Watercolor Guide | https://www.artistsnetwork.com/art-mediums/watercolor/ |
| Acrylic Painting | https://www.artistsnetwork.com/art-mediums/acrylic/ |
| Oil Painting | https://www.artistsnetwork.com/art-mediums/oil-painting/ |
| Gouache | https://www.artistsnetwork.com/art-mediums/gouache/ |
| Tempera | https://www.britannica.com/art/tempera-painting |
| Encaustic | https://www.artistsnetwork.com/art-mediums/encaustic/ |

## Printmaking
| Medium | URL |
|--------|-----|
| Linocut | https://www.moma.org/collection/terms/linocut |
| Etching | https://www.metmuseum.org/about-the-met/collection-areas/drawings-and-prints/etching |
| Screen Printing | https://www.moma.org/collection/terms/screenprint |
| Woodcut | https://www.metmuseum.org/toah/hd/wdct/hd_wdct.htm |
| Lithography | https://www.metmuseum.org/toah/hd/lith/hd_lith.htm |

## Paper & Surfaces
| Material | URL |
|----------|-----|
| Paper Types Guide | https://www.artistsnetwork.com/art-mediums/drawing/paper-types/ |
| Canvas Preparation | https://www.artistsnetwork.com/art-mediums/oil-painting/canvas-prep/ |
| Drawing Boards | https://www.artistsnetwork.com/art-mediums/drawing/drawing-boards/ |
| Alternative Surfaces | https://www.artistsnetwork.com/art-techniques/alternative-surfaces/ |
'''

for path, content in files.items():
    full_path = os.path.join(base, path)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print(f'\nDone! All 20 folders now have reference files.')
"