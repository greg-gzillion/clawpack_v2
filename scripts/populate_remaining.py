import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\drawclaw"
files = {}

# Production pipelines
files["production/concept_art_pipeline/concept_art_pipeline.md"] = """# Concept Art Pipeline
| Stage | Description | Resource |
|-------|-------------|----------|
| Brief | Understanding requirements | https://www.creativebloq.com/career/concept-artist-11121137 |
| Research | Reference gathering | https://www.artstation.com/learning |
| Thumbnails | Quick ideation sketches | https://www.fzdschool.com/ |
| Roughs | Selected concepts refined | https://www.thegnomonworkshop.com/ |
| Final | Polished presentation | https://www.learnsquared.com/ |
"""

files["production/game_art_pipeline/game_art_pipeline.md"] = """# Game Art Pipeline
| Stage | Description | Resource |
|-------|-------------|----------|
| Pre-production | Style guides, mood boards | https://www.artstation.com/channels/game_art |
| Modeling | 3D asset creation | https://www.blender.org/ |
| Texturing | Surface detail | https://www.creativebloq.com/3d/texturing |
| Implementation | Engine integration | https://www.unrealengine.com/ |
"""

files["production/illustration_pipeline/illustration_pipeline.md"] = """# Illustration Pipeline
| Stage | Resource |
|-------|----------|
| Thumbnails | https://www.artistsnetwork.com/art-techniques/composition/ |
| Sketch | https://www.creativebloq.com/illustration/ |
| Values | https://www.artistsnetwork.com/art-techniques/value-drawing/ |
| Color | https://www.color-meanings.com/ |
| Final | https://www.artstation.com/learning/ |
"""

files["production/visual_development/visual_development.md"] = """# Visual Development
| Resource | URL |
|----------|-----|
| VisDev Process | https://www.creativebloq.com/animation/visual-development-11121137 |
| Color Scripts | https://www.artofthetitle.com/ |
| Style Guides | https://www.artstation.com/channels/visual_development |
"""

# Perspective Advanced
files["perspective_advanced/architecture_perspective/architecture_perspective.md"] = """# Architecture Perspective
| Resource | URL |
|----------|-----|
| Architectural Drawing Guide | https://www.artistsnetwork.com/art-mediums/drawing/architectural-drawing/ |
| How to Draw Buildings | https://www.creativebloq.com/art/how-draw-buildings |
| Urban Sketching | https://urbansketchers.org/ |
"""

files["perspective_advanced/interior_perspective/interior_perspective.md"] = """# Interior Perspective
| Resource | URL |
|----------|-----|
| Interior Drawing Guide | https://www.artistsnetwork.com/art-mediums/drawing/interior-drawing/ |
| Room Perspective Tutorial | https://www.studentartguide.com/articles/one-point-perspective-drawing |
| Furniture Rendering | https://www.creativebloq.com/interior-design |
"""

files["perspective_advanced/vehicle_perspective/vehicle_perspective.md"] = """# Vehicle Perspective
| Resource | URL |
|----------|-----|
| Vehicle Design Tutorial | https://www.creativebloq.com/illustration/vehicle-design |
| How to Draw Cars | https://www.artistsnetwork.com/art-mediums/drawing/car-drawing/ |
| Scott Robertson Vehicle | https://www.goodreads.com/book/show/15061468-how-to-draw |
"""

files["perspective_advanced/cinematic_camera/cinematic_camera.md"] = """# Cinematic Camera Angles
| Resource | URL |
|----------|-----|
| Camera Angles Guide | https://www.studiobinder.com/blog/types-of-camera-shot-angles/ |
| Shot Composition | https://www.studiobinder.com/blog/rules-of-shot-composition/ |
| Film Framing Techniques | https://www.studiobinder.com/blog/types-of-camera-framing/ |
"""

# Entertainment Art
files["entertainment_art/creature_design/creature_design.md"] = """# Creature Design
| Resource | URL |
|----------|-----|
| Creature Anatomy | https://www.creativebloq.com/3d/creature-design-tips |
| Terryl Whitlatch | https://www.creatureanatomy.com/ |
| Monster Design Tips | https://www.creativebloq.com/illustration/creature-design |
"""

files["entertainment_art/prop_design/prop_design.md"] = """# Prop Design
| Resource | URL |
|----------|-----|
| Prop Design Tutorial | https://www.artstation.com/learning/courses/ |
| Weapon Design | https://www.creativebloq.com/digital-art/weapon-design-tips |
"""

files["entertainment_art/costume_design/costume_design.md"] = """# Costume Design
| Resource | URL |
|----------|-----|
| Costume Design for Characters | https://www.creativebloq.com/fashion/character-costume-design |
| Fashion Illustration | https://www.creativebloq.com/fashion/fashion-illustration |
"""

files["entertainment_art/cinematic_keyframes/cinematic_keyframes.md"] = """# Cinematic Keyframes
| Resource | URL |
|----------|-----|
| Keyframe Illustration | https://www.creativebloq.com/animation/keyframe |
| Color Scripts | https://www.artofthetitle.com/ |
"""

# Sequential Art
files["sequential_art/comic_panels/comic_panels.md"] = """# Comic Panels
| Resource | URL |
|----------|-----|
| Comic Panel Layout | https://www.creativebloq.com/comics/panel-layout |
| Making Comics (Scott McCloud) | https://www.goodreads.com/book/show/75332.Making_Comics |
"""

files["sequential_art/visual_storytelling/visual_storytelling.md"] = """# Visual Storytelling
| Resource | URL |
|----------|-----|
| Visual Storytelling Guide | https://www.creativebloq.com/illustration/narrative-art |
| Storytelling Through Art | https://www.artofthetitle.com/ |
"""

files["sequential_art/shot_composition/shot_composition.md"] = """# Shot Composition
| Resource | URL |
|----------|-----|
| Shot Composition Rules | https://www.studiobinder.com/blog/rules-of-shot-composition/ |
| Framing Guide | https://www.studiobinder.com/blog/types-of-camera-framing/ |
"""

# Commercial Art
files["commercial_art/advertising_design/advertising_design.md"] = """# Advertising Design
| Resource | URL |
|----------|-----|
| Advertising Illustration | https://www.creativebloq.com/illustration/advertising |
| Commercial Art Guide | https://www.creativebloq.com/graphic-design/advertising |
"""

files["commercial_art/editorial_illustration/editorial_illustration.md"] = """# Editorial Illustration
| Resource | URL |
|----------|-----|
| Editorial Illustration Guide | https://www.creativebloq.com/illustration/editorial-illustration |
| Magazine Illustration | https://www.artistsnetwork.com/art-mediums/illustration/editorial/ |
"""

# Mastery
files["mastery/contemporary_professionals/contemporary_professionals.md"] = """# Contemporary Professionals
| Artist | URL |
|--------|-----|
| ArtStation Top Artists | https://www.artstation.com/ |
| Feng Zhu | https://www.fzdschool.com/ |
| Loish | https://loish.net/ |
| Craig Mullins | https://www.goodbrush.com/ |
"""

files["mastery/industry_interviews/industry_interviews.md"] = """# Industry Interviews
| Resource | URL |
|----------|-----|
| Proko Draftsmen Podcast | https://www.youtube.com/@Draftsmen |
| Bobby Chiu Interviews | https://www.youtube.com/@BobbyChiu |
| Lightbox Expo Talks | https://www.lightboxexpo.com/ |
"""

# Teaching
files["teaching/beginner_to_advanced/beginner_to_advanced.md"] = """# Beginner to Advanced Path
| Resource | URL |
|----------|-----|
| Draw A Box (Free Complete Course) | https://drawabox.com/ |
| Ctrl+Paint (Digital Art) | https://www.ctrlpaint.com/library |
| Proko Figure Drawing | https://www.proko.com/course/figure-drawing-fundamentals/ |
"""

files["teaching/critique_frameworks/critique_frameworks.md"] = """# Critique Frameworks
| Resource | URL |
|----------|-----|
| How to Give Art Critique | https://www.artistsnetwork.com/art-critique/ |
| Art Critique Method | https://www.creativebloq.com/career/art-director-feedback |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files across all empty folders.")
