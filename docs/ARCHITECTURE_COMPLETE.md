# 🦞 CLAWPACK V2 - COMPLETE ARCHITECTURE REFERENCE
## Every File, Every Folder, Every Function

**Generated:** 2026-04-23 01:23:57
**Location:** C:\Users\greg\dev\clawpack_v2
**Total Size:** ~160 GB

---

## 📁 COMPLETE DIRECTORY TREE
├── 📁 .git/
├── 📁 hooks/
├── 📄 applypatch-msg.sample (478 B)
├── 📄 commit-msg.sample (896 B)
├── 📄 fsmonitor-watchman.sample (4.62 KB)
├── 📄 post-update.sample (189 B)
├── 📄 pre-applypatch.sample (424 B)
├── 📄 pre-commit.sample (1.61 KB)
├── 📄 pre-merge-commit.sample (416 B)
├── 📄 prepare-commit-msg.sample (1.46 KB)
├── 📄 pre-push.sample (1.34 KB)
├── 📄 pre-rebase.sample (4.78 KB)
├── 📄 pre-receive.sample (544 B)
├── 📄 push-to-checkout.sample (2.72 KB)
├── 📄 sendemail-validate.sample (2.25 KB)
└── 📄 update.sample (3.56 KB)
├── 📁 info/
├── 📄 exclude (240 B)
└── 📄 refs (437 B)
├── 📁 logs/
├── 📁 refs/
├── 📁 heads/
└── 📄 main (9.24 KB)
└── 📁 remotes/
└── 📁 origin/
├── 📄 HEAD (131 B)
└── 📄 main (5.89 KB)
└── 📄 HEAD (9.55 KB)
├── 📁 modules/
└── 📁 references/
└── 📁 common_chronicle/
├── 📁 hooks/
├── 📄 applypatch-msg.sample (478 B)
├── 📄 commit-msg.sample (896 B)
├── 📄 fsmonitor-watchman.sample (4.62 KB)
├── 📄 post-checkout (360 B)
├── 📄 post-commit (356 B)
├── 📄 post-merge (354 B)
├── 📄 post-update.sample (189 B)
├── 📄 pre-applypatch.sample (424 B)
├── 📄 pre-commit.sample (1.61 KB)
├── 📄 pre-merge-commit.sample (416 B)
├── 📄 prepare-commit-msg.sample (1.46 KB)
├── 📄 pre-push (350 B)
├── 📄 pre-push.sample (1.34 KB)
├── 📄 pre-rebase.sample (4.78 KB)
├── 📄 pre-receive.sample (544 B)
├── 📄 push-to-checkout.sample (2.72 KB)
├── 📄 sendemail-validate.sample (2.25 KB)
└── 📄 update.sample (3.56 KB)
├── 📁 info/
└── 📄 exclude (240 B)
├── 📁 lfs/
├── 📁 incomplete/
├── 📁 objects/
└── 📁 tmp/
├── 📁 logs/
├── 📁 refs/
└── 📄 HEAD (198 B)
├── 📁 objects/
├── 📁 info/
└── 📁 pack/
├── 📁 refs/
├── 📁 heads/
├── 📁 remotes/
└── 📁 tags/
├── 📄 config (406 B)
├── 📄 description (73 B)
├── 📄 HEAD (21 B)
├── 📄 index (17.93 KB)
└── 📄 packed-refs (112 B)
├── 📁 objects/
├── 📁 02/
└── 📄 f5a4ce174ab7a57730da721ef38a0ae8feb6d1 (55 B)
├── 📁 03/
└── 📄 c2d46386e1f282f491db5c5c4992874f1adddb (240 B)
├── 📁 08/
└── 📄 a4190e36ddc95250011bb44ab3141f54957fb2 (535 B)
├── 📁 0f/
└── 📄 5ae6137339c196f2468be7c1c118ac3378fc0d (556 B)
├── 📁 14/
└── 📄 ae9ca169d1fa9116195a23d0b90d3ba3d279b3 (879 B)
├── 📁 15/
└── 📄 94ffb1d6f7a1505a44fafa6e5ebaf401fc0891 (2.44 KB)
├── 📁 18/
└── 📄 33762991239e67a19cc71945e9b2b975a4d41b (1.15 KB)
├── 📁 1b/
└── 📄 17a2602cd6d7332e4910074b00b7e62a90d3eb (556 B)
├── 📁 1c/
└── 📄 2f76d496df9efa5d61b4756238d19696f593d1 (226 B)
├── 📁 1e/
└── 📄 7bbfa820e7246176d1c50e1818c86905415e09 (910 B)
├── 📁 24/
└── 📄 785e9bf7c57abb1bb92ae6f37938fdc2264c7e (658 B)
├── 📁 25/
├── 📄 0d6eaf9b4b823de17c62c22268f208455bd0cc (730 B)
└── 📄 6076833bfde94d59c87999a596165ca1c1127b (60 B)
├── 📁 26/
└── 📄 492ae506fe556a8f25f3d25d16d6d2b6bb8b7d (538 B)
├── 📁 29/
└── 📄 7c6d57a4c5346108aefca7630a001064e14dad (807 B)
├── 📁 2b/
└── 📄 4940c59feaa87fd2c5d1583a5d77a99ef7a0f2 (405 B)
├── 📁 30/
├── 📄 25223daa9786060e027f5031abe0146055569e (442 B)
└── 📄 49cdc02a666e637ffcacf1a2b0fcbe9f1ea6ac (500 B)
├── 📁 3d/
├── 📄 0b0477ae2fa03f1514bd85f8c94d8931db4dc5 (2.05 KB)
├── 📄 0f520c66bcf895194494e4a281a367587c6f33 (271 B)
└── 📄 46300d89c7dd9cd7d3131e92b27b683960bb76 (793 B)
├── 📁 4c/
├── 📄 d72e4789704c0319865727ca5044183c09b1a9 (411 B)
└── 📄 f9bb27b5ea031281fec1f89f72373bfe75d44f (495 B)
├── 📁 4d/
├── 📄 69d506034b9dac27680de334713b17964f6eb5 (209 B)
└── 📄 6c0e1deb11c4e482ec48535b56f2a9c87a48d4 (664 B)
├── 📁 4e/
└── 📄 cdef5504c726e703fdd7ee66c35a1e6e8dee27 (207 B)
├── 📁 52/
├── 📄 9f335183404618f98a5b4d090e2a48a46d901b (479 B)
└── 📄 e0c23a5a37455f259ebf040260c7104821ef55 (378 B)
├── 📁 53/
└── 📄 f50cf1147bc3f083b1fe6f18c8945a3d8b92d3 (476 B)
├── 📁 54/
└── 📄 e1654948e0d8e6201cf9edb252e9639bd461e7 (194 B)
├── 📁 57/
└── 📄 cee59e824a884716babbcc279c243946501d3a (490 B)
├── 📁 59/
└── 📄 ef9dd961dbc965089aeed6a7bceb62deb49e1a (56 B)
├── 📁 61/
└── 📄 12e37d74abbe253fa1ad4930299a1fda22b96d (1.37 KB)
├── 📁 62/
└── 📄 fec8edf84a275952c793656ba0ba58e2059fb9 (404 B)
├── 📁 64/
└── 📄 897cfd306fdc7f620f977abf83960f13c82c20 (825 B)
├── 📁 66/
└── 📄 cf8d6c025c4ccc38b8dd66b07cf1e87556a7cf (641 B)
├── 📁 69/
├── 📄 3ea6111c395a321c41c41b52806a68078673bb (1.51 KB)
└── 📄 940d386d0c88d1c956c2d0b94bd46ac411062b (376 B)
├── 📁 6a/
├── 📄 6adb5835a2194d26919cc9a7b5dd6b9fc42b2e (282 B)
└── 📄 d21f371c275d96a091d65d5da9af4f86885e56 (1.22 KB)
├── 📁 71/
└── 📄 4d1e9bfb9f8d2a2b7f3623a4869b5d2460fce5 (683 B)
├── 📁 72/
└── 📄 b5dbd1e021918eb5069fd7182c5b7fc7a3ce1c (518 B)
├── 📁 78/
└── 📄 c938b386e3058ca20ed0dd7f74b91bb29b8452 (399 B)
├── 📁 7d/
└── 📄 4117a47ecf31dd8457d019d2a1bf35e114e126 (368 B)
├── 📁 84/
├── 📄 80b0f513b74410c17a06a3bf459fa919b805a6 (122 B)
└── 📄 c82779e8e1caa885baff43b07638cd855c7626 (378 B)
├── 📁 85/
└── 📄 cd8bca72857c7de8be351f4afdbf528d97e7ae (3.07 KB)
├── 📁 8a/
└── 📄 e9ce8995fba49b764583e71188be649e6dd4fa (144 B)
├── 📁 8f/
└── 📄 82188a35e268bb2b46ddb252267e145fd686d2 (1.19 KB)
├── 📁 a2/
└── 📄 de1d8970b541c3bb0f9f765b3fff8c23881245 (64 B)
├── 📁 a6/
└── 📄 87101546e523da0f94828901b9df3bc307db7e (977 B)
├── 📁 a8/
└── 📄 1170d916f3fbf1a1aeec4d43112aab2c1b4e94 (271 B)
├── 📁 aa/
└── 📄 086b64098aa719fac78c6d5907eef42782fa54 (519 B)
├── 📁 ac/
└── 📄 a42e25c2cb8d19ea3914c789bf844dd60ae397 (1.38 KB)
├── 📁 ad/
└── 📄 6b91d162308cba40a5da5de03d446beb6bac3d (386 B)
├── 📁 ae/
└── 📄 6a58b4b384f217e8ad503fa49fe4933e0a081e (692 B)
├── 📁 b3/
└── 📄 e97366372e3116bbb25e189486b438a87449ac (508 B)
├── 📁 b6/
└── 📄 91b7b5fe439ed00c7d099d9cd702b09786915d (692 B)
├── 📁 b9/
└── 📄 315b86bc51a905f57b9e66c683dce9141fa14f (830 B)
├── 📁 bd/
└── 📄 df1ac6ddbb6be43de9cae3fff7fcd014bc547d (983 B)
├── 📁 c0/
└── 📄 4d1b21052cdb6c7d8f75cfe59d894417e8e24f (206 B)
├── 📁 c5/
└── 📄 8ba4303b5d1741523aa0d0687e208943e95dc6 (397 B)
├── 📁 c6/
├── 📄 11f501861adbf4e4fdef12e28436e9b991da79 (692 B)
└── 📄 e31e4614d9a86424e0a1942bbffbc4afe570c7 (125 B)
├── 📁 ca/
└── 📄 376b9511f5092a56224029fd2c2be39828c6a4 (355 B)
├── 📁 cb/
└── 📄 2c78fbdcd5b66fc358c6a9445876285e81bc4d (63 B)
├── 📁 d0/
└── 📄 822bbb93254a23b6e79c6e4a4589c4e6756ce2 (1024 B)
├── 📁 d2/
└── 📄 e33a4cafb572fec079ff13ae6dd9070d49acf8 (794 B)
├── 📁 d5/
└── 📄 7f9144d536b49ce39f69bbdeb1ab9d5cf2e6b6 (247 B)
├── 📁 d6/
└── 📄 93d9fc00cde86a0e0028154c5d19a661b1d59f (207 B)
├── 📁 da/
└── 📄 314b4beb6d8f59ffb93361c7c376376c984e0f (1.1 KB)
├── 📁 db/
└── 📄 9553e021b6a077a89ce87044f34bd72c074a87 (282 B)
├── 📁 e4/
└── 📄 7f21b36f08f2d7e523223175ffc603e0dfb304 (244 B)
├── 📁 e6/
├── 📄 4caa6481c2dcf02480ab7529f84de345f98db2 (207 B)
└── 📄 ba5d8f911e0d9d1b9eb70a4b05b3569898ebfe (650 B)
├── 📁 e9/
└── 📄 0535940a48ceec0d1b39516809d97eee3c6dcf (418 B)
├── 📁 f8/
└── 📄 ff0f68a46aee7ae9bc0b24f4a610dbd724298d (3.11 KB)
├── 📁 fd/
└── 📄 1e6b0f302a43b25b5f3a16276cc9fed71c1e85 (409 B)
├── 📁 info/
├── 📄 commit-graph (4.89 KB)
└── 📄 packs (160 B)
└── 📁 pack/
├── 📄 pack-0ee292d59414c281fea791351b491e83ed5413a4.idx (563.4 KB)
├── 📄 pack-0ee292d59414c281fea791351b491e83ed5413a4.pack (5.51 MB)
├── 📄 pack-0ee292d59414c281fea791351b491e83ed5413a4.rev (80.39 KB)
├── 📄 pack-6dc1df1a2fd41688d7e332fa026462ff95b78391.idx (28.47 KB)
├── 📄 pack-6dc1df1a2fd41688d7e332fa026462ff95b78391.pack (368.3 KB)
├── 📄 pack-6dc1df1a2fd41688d7e332fa026462ff95b78391.rev (3.97 KB)
├── 📄 pack-d2336a45167e60f31ea9b55b7d2ba87ccc5696de.idx (265.11 KB)
├── 📄 pack-d2336a45167e60f31ea9b55b7d2ba87ccc5696de.pack (9.55 MB)
└── 📄 pack-d2336a45167e60f31ea9b55b7d2ba87ccc5696de.rev (37.77 KB)
├── 📁 refs/
├── 📁 heads/
└── 📄 main (41 B)
├── 📁 remotes/
└── 📁 origin/
├── 📄 HEAD (30 B)
└── 📄 main (41 B)
└── 📁 tags/
├── 📄 v1.0-txclaw (41 B)
└── 📄 v2.0.0 (41 B)
├── 📄 COMMIT_EDITMSG (544 B)
├── 📄 config (432 B)
├── 📄 description (73 B)
├── 📄 FETCH_HEAD (104 B)
├── 📄 HEAD (21 B)
├── 📄 index (3.16 MB)
└── 📄 ORIG_HEAD (41 B)
├── 📁 .github/
├── 📁 ISSUE_TEMPLATE/
├── 📄 bug_report.md (611 B)
└── 📄 feature_request.md (555 B)
└── 📁 workflows/
└── 📄 codeql.yml (593 B)
├── 📁 agents/
├── 📁 claw_coder/
├── 📁 agents/
├── 📄 dataclaw_client.py (959 B)
└── 📄 webclaw_client.py (917 B)
├── 📁 cli/
├── 📄 __init__.py (65 B)
└── 📄 parser.py (162 B)
├── 📁 commands/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (165 B)
├── 📄 code.cpython-312.pyc (2.99 KB)
├── 📄 code_direct.cpython-312.pyc (1.12 KB)
├── 📄 debug.cpython-312.pyc (1.28 KB)
├── 📄 explain.cpython-312.pyc (1.27 KB)
├── 📄 review.cpython-312.pyc (1.29 KB)
└── 📄 tutorial.cpython-312.pyc (1.31 KB)
├── 📄 __init__.py (27 B)
├── 📄 code.py (1.89 KB)
├── 📄 code_direct.py (686 B)
├── 📄 debug.py (673 B)
├── 📄 explain.py (666 B)
├── 📄 review.py (687 B)
├── 📄 system.py (355 B)
└── 📄 tutorial.py (703 B)
├── 📁 engine/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (296 B)
└── 📄 programming_engine.cpython-312.pyc (5.47 KB)
├── 📄 __init__.py (118 B)
├── 📄 base_language.py (903 B)
├── 📄 data.py (187 B)
├── 📄 llm_wrapper.py (823 B)
├── 📄 memory.py (1.95 KB)
├── 📄 orchestrator.py (3.81 KB)
└── 📄 programming_engine.py (3.47 KB)
├── 📁 languages/
├── 📄 assembly.py (1.17 KB)
├── 📄 bash.py (1.14 KB)
├── 📄 batch.py (1.14 KB)
├── 📄 c.py (1.4 KB)
├── 📄 clojure.py (1.46 KB)
├── 📄 cobol.py (1.14 KB)
├── 📄 cpp.py (1.56 KB)
├── 📄 csharp.py (1.46 KB)
├── 📄 dart.py (1.42 KB)
├── 📄 elixir.py (1.44 KB)
├── 📄 erlang.py (1.44 KB)
├── 📄 fortran.py (1.17 KB)
├── 📄 go.py (1.47 KB)
├── 📄 groovy.py (1.45 KB)
├── 📄 haskell.py (1.45 KB)
├── 📄 html.py (1.14 KB)
├── 📄 java.py (1.44 KB)
├── 📄 javascript.py (1.49 KB)
├── 📄 julia.py (1.13 KB)
├── 📄 kotlin.py (1.45 KB)
├── 📄 lua.py (1.41 KB)
├── 📄 makefile.py (1.17 KB)
├── 📄 matlab.py (1.15 KB)
├── 📄 nim.py (1.12 KB)
├── 📄 objectivec.py (1.48 KB)
├── 📄 perl.py (1.42 KB)
├── 📄 php.py (1.41 KB)
├── 📄 powershell.py (1.18 KB)
├── 📄 python.py (1.75 KB)
├── 📄 r.py (1.39 KB)
├── 📄 ruby.py (1.42 KB)
├── 📄 rust.py (1.52 KB)
├── 📄 scala.py (1.44 KB)
├── 📄 sql.py (1.43 KB)
├── 📄 swift.py (1.43 KB)
├── 📄 typescript.py (1.49 KB)
├── 📄 vhdl.py (1.14 KB)
├── 📄 yaml.py (1.13 KB)
└── 📄 zig.py (1.12 KB)
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
├── 📄 claw_coder.py (2.14 KB)
├── 📄 core_link (10 B)
├── 📄 hooks.py (1.26 KB)
├── 📄 test_ai.py (789 B)
├── 📄 test_discovery.py (1.08 KB)
└── 📄 test_import.py (538 B)
├── 📁 crustyclaw/
├── 📁 integrations/
└── 📄 chronicle_bridge.rs (3.55 KB)
├── 📁 src/
├── 📄 a2a.rs (2.19 KB)
├── 📄 chronicle_commands.rs (3.17 KB)
├── 📄 lib.rs (553 B)
├── 📄 main.rs (5.44 KB)
├── 📄 memory.rs (3.68 KB)
└── 📄 security.rs (1.91 KB)
├── 📄 Cargo.toml (1.3 KB)
└── 📄 chronicle_bridge.py (2.89 KB)
├── 📁 dataclaw/
├── 📁 cli/
├── 📄 __init__.py (65 B)
└── 📄 parser.py (162 B)
├── 📁 commands/
├── 📄 __init__.py (25 B)
├── 📄 data.py (449 B)
└── 📄 system.py (355 B)
├── 📁 core/
├── 📄 __init__.py (63 B)
└── 📄 data.py (181 B)
├── 📁 modules/
├── 📁 indexer/
├── 📄 __init__.py (41 B)
└── 📄 local_indexer.py (228 B)
├── 📁 integration/
└── 📄 agent_hub.py (2.78 KB)
├── 📁 metadata/
└── 📄 extractor.py (2.98 KB)
├── 📁 scanner/
├── 📄 __init__.py (39 B)
└── 📄 file_scanner.py (333 B)
├── 📁 search/
├── 📄 __init__.py (39 B)
└── 📄 local_search.py (214 B)
└── 📄 __init__.py (24 B)
├── 📁 references/
├── 📁 algorithms/
└── 📄 README.md (287 B)
├── 📁 big_data/
└── 📄 README.md (283 B)
├── 📁 data_structures/
└── 📄 README.md (297 B)
├── 📁 data_visualization/
└── 📄 README.md (303 B)
├── 📁 data_warehousing/
└── 📄 README.md (299 B)
├── 📁 etl/
└── 📄 README.md (273 B)
├── 📁 machine_learning/
└── 📄 README.md (299 B)
├── 📁 nosql/
└── 📄 README.md (277 B)
├── 📁 sql/
└── 📄 README.md (273 B)
├── 📄 data_index.db (16 KB)
├── 📄 sample_data.md (321 B)
└── 📄 sample_legal_data.md (317 B)
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
└── 📄 dataclaw.py (1.06 KB)
├── 📁 designclaw/
├── 📁 __pycache__/
└── 📄 __init__.cpython-312.pyc (156 B)
├── 📁 cli/
└── 📄 __init__.py (32 B)
├── 📁 commands/
└── 📄 logo.py (1.71 KB)
├── 📁 core/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (161 B)
└── 📄 agent.cpython-312.pyc (7.35 KB)
├── 📄 __init__.py (0 B)
└── 📄 agent.py (5.37 KB)
├── 📁 data/
└── 📄 shared_memory.json (107 B)
├── 📁 exports/
├── 📁 providers/
└── 📄 __init__.py (38 B)
├── 📁 utils/
├── 📄 __init__.py (133 B)
├── 📄 input_handler.py (3.8 KB)
└── 📄 preview.py (6.91 KB)
├── 📄 .env (0 B)
├── 📄 __init__.py (0 B)
├── 📄 designclaw.py (1.15 KB)
└── 📄 README.md (5.61 KB)
├── 📁 docuclaw/
├── 📁 cli/
├── 📄 __init__.py (65 B)
└── 📄 parser.py (162 B)
├── 📁 commands/
├── 📄 analyze.py (553 B)
├── 📄 batchprint.py (912 B)
├── 📄 codesearch.py (1.2 KB)
├── 📄 codestats.py (1.4 KB)
├── 📄 create.py (1.02 KB)
├── 📄 csvtable.py (798 B)
├── 📄 diagram.py (236 B)
├── 📄 diff.py (1.16 KB)
├── 📄 doc.py (461 B)
├── 📄 draft.py (1.38 KB)
├── 📄 export.py (570 B)
├── 📄 exportapp.py (3.04 KB)
├── 📄 flowchart.py (260 B)
├── 📄 footer.py (602 B)
├── 📄 footnote.py (698 B)
├── 📄 formatcode.py (1.13 KB)
├── 📄 header.py (612 B)
├── 📄 help.py (1.88 KB)
├── 📄 highlight.py (2.33 KB)
├── 📄 import.py (2.28 KB)
├── 📄 layout.py (729 B)
├── 📄 pagenum.py (556 B)
├── 📄 print.py (1.78 KB)
├── 📄 printfile.py (984 B)
├── 📄 quit.py (72 B)
├── 📄 review.py (729 B)
├── 📄 table.py (756 B)
├── 📄 templates.py (446 B)
├── 📄 toc.py (850 B)
├── 📄 topdf.py (1.28 KB)
└── 📄 translate.py (2.71 KB)
├── 📁 core/
├── 📄 base.py (255 B)
└── 📄 config.py (211 B)
├── 📁 importers/
├── 📄 base.py (277 B)
├── 📄 csv.py (861 B)
├── 📄 docx.py (975 B)
├── 📄 html.py (876 B)
├── 📄 json.py (788 B)
├── 📄 markdown.py (945 B)
├── 📄 odt.py (967 B)
├── 📄 pdf.py (1007 B)
├── 📄 rtf.py (702 B)
├── 📄 text.py (603 B)
└── 📄 xml.py (775 B)
├── 📁 imports/
└── 📄 imported_sample_import_20260410_202059.md (13 B)
├── 📁 modules/
├── 📁 __pycache__/
└── 📄 __init__.cpython-312.pyc (193 B)
├── 📁 ai/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (213 B)
└── 📄 assistant.cpython-312.pyc (747 B)
├── 📄 __init__.py (36 B)
└── 📄 assistant.py (222 B)
├── 📁 export/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (217 B)
└── 📄 handler.cpython-312.pyc (564 B)
├── 📄 __init__.py (36 B)
└── 📄 handler.py (119 B)
├── 📁 formatter/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (215 B)
└── 📄 styles.cpython-312.pyc (561 B)
├── 📄 __init__.py (31 B)
└── 📄 styles.py (135 B)
├── 📁 media/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (215 B)
└── 📄 handler.cpython-312.pyc (554 B)
├── 📄 __init__.py (35 B)
└── 📄 handler.py (113 B)
├── 📁 templates/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (244 B)
└── 📄 docs.cpython-312.pyc (649 B)
├── 📄 __init__.py (48 B)
└── 📄 docs.py (207 B)
└── 📄 __init__.py (24 B)
├── 📁 output/
├── 📄 ai_letter_20260410_204115.html (350 B)
├── 📄 ai_letter_20260410_204158.html (487 B)
├── 📄 ai_letter_20260410_204231.html (267 B)
├── 📄 ai_letter_20260410_204315.html (1.92 KB)
├── 📄 ai_letter_20260410_204344.html (1.93 KB)
├── 📄 ai_letter_20260410_204619.html (277 B)
├── 📄 ai_letter_20260410_204712.html (269 B)
├── 📄 ai_letter_20260410_204759.html (277 B)
├── 📄 ai_letter_20260410_204847.html (269 B)
├── 📄 ai_letter_20260410_205147.html (1.04 KB)
├── 📄 ai_letter_20260410_205426.html (379 B)
├── 📄 ai_letter_20260410_205510.html (2.54 KB)
├── 📄 ai_letter_20260410_205547.html (471 B)
├── 📄 ai_letter_20260410_205644.html (2.66 KB)
├── 📄 ai_letter_20260410_205948.html (1.87 KB)
├── 📄 ai_letter_20260410_210021.html (2.01 KB)
├── 📄 ai_letter_20260410_210100.html (2.42 KB)
├── 📄 ai_meeting_notes_20260410_204351.html (2.33 KB)
├── 📄 ai_memo_20260410_203926.html (350 B)
├── 📄 ai_memo_20260410_204051.html (350 B)
├── 📄 ai_memo_20260410_204115.html (347 B)
├── 📄 ai_memo_20260410_204349.html (2.55 KB)
├── 📄 ai_report_20260410_203611.html (237 B)
├── 📄 ai_report_20260410_203700.html (535 B)
├── 📄 ai_report_20260410_203744.html (1.09 KB)
├── 📄 ai_report_20260410_203926.html (352 B)
├── 📄 ai_report_20260410_204115.html (351 B)
├── 📄 ai_report_20260410_204347.html (3.56 KB)
├── 📄 letter_20260410_202024.json (364 B)
├── 📄 letter_20260410_202024.md (220 B)
├── 📄 letter_20260410_202024.pdf.html (674 B)
├── 📄 letter_20260410_202308.md (226 B)
├── 📄 letter_20260410_203611.html (335 B)
└── 📄 sample_letter_20260410.md (173 B)
├── 📁 processors/
├── 📄 json.py (330 B)
├── 📄 markdown.py (284 B)
└── 📄 text.py (273 B)
├── 📁 session/
└── 📄 session_manager.py (2.4 KB)
├── 📁 templates/
├── 📁 business/
├── 📄 letter.md (173 B)
├── 📄 meeting_minutes.md (232 B)
└── 📄 proposal.md (235 B)
├── 📁 education/
├── 📄 lesson_plan.md (240 B)
└── 📄 research_paper.md (300 B)
├── 📁 personal/
├── 📄 cover_letter.md (190 B)
├── 📄 resume.md (213 B)
└── 📄 todo.md (209 B)
└── 📁 technical/
├── 📄 api_docs.md (248 B)
├── 📄 code_review.md (257 B)
└── 📄 readme.md (215 B)
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
├── 📄 data.csv (72 B)
├── 📄 data_table.md (120 B)
├── 📄 diagram_20260408_123244.txt (98 B)
├── 📄 docuclaw.py (547 B)
├── 📄 docuclaw_clean.py (10.02 KB)
├── 📄 flowchart_20260408_123244.txt (0 B)
├── 📄 letter_20260408_123244.md (125 B)
├── 📄 media_importer.py (7.41 KB)
├── 📄 sample.md (289 B)
├── 📄 sample_layouted.md (355 B)
├── 📄 sample_numbered.md (326 B)
├── 📄 sample_with_footer.md (338 B)
├── 📄 sample_with_header.md (347 B)
├── 📄 sample_with_toc.md (422 B)
├── 📄 session_manager.py (2.39 KB)
└── 📄 table_3x4.md (70 B)
├── 📁 draftclaw/
├── 📁 cli/
└── 📄 __init__.py (31 B)
├── 📁 commands/
└── 📄 blueprint.py (1.94 KB)
├── 📁 core/
├── 📄 __init__.py (32 B)
└── 📄 agent.py (2.46 KB)
├── 📁 exports/
├── 📁 providers/
└── 📄 __init__.py (37 B)
├── 📁 utils/
└── 📄 __init__.py (33 B)
└── 📄 draftclaw.py (1.71 KB)
├── 📁 drawclaw/
├── 📁 core/
└── 📄 agent.py (1.83 KB)
├── 📁 exports/
└── 📄 drawclaw.py (1.88 KB)
├── 📁 dreamclaw/
├── 📁 cli/
└── 📄 __init__.py (31 B)
├── 📁 commands/
└── 📄 dream.py (1.55 KB)
├── 📁 core/
├── 📄 __init__.py (32 B)
└── 📄 agent.py (6.6 KB)
├── 📁 exports/
├── 📁 providers/
└── 📄 __init__.py (37 B)
├── 📁 utils/
└── 📄 __init__.py (33 B)
└── 📄 dreamclaw.py (1.71 KB)
├── 📁 fileclaw/
├── 📁 commands/
└── 📄 __init__.py (0 B)
├── 📁 core/
└── 📄 __init__.py (0 B)
├── 📁 handlers/
└── 📄 __init__.py (0 B)
├── 📁 modules/
└── 📄 __init__.py (0 B)
├── 📁 utils/
└── 📄 __init__.py (0 B)
└── 📄 fileclaw.py (15.72 KB)
├── 📁 flowclaw/
├── 📁 cli/
└── 📄 __init__.py (30 B)
├── 📁 commands/
├── 📄 flowchart.py (1.91 KB)
└── 📄 mindmap.py (837 B)
├── 📁 core/
├── 📄 __init__.py (31 B)
└── 📄 agent.py (1.52 KB)
├── 📁 engine/
├── 📄 __init__.py (0 B)
├── 📄 diagram_engine.py (2.18 KB)
├── 📄 diagram_processor.py (1.28 KB)
├── 📄 diagram_types.py (2 KB)
├── 📄 high_res_renderer.py (11.44 KB)
├── 📄 mermaid_validator.py (1.53 KB)
├── 📄 syntax_cleaner.py (1.16 KB)
└── 📄 syntax_validator.py (2.42 KB)
├── 📁 exporters/
├── 📄 __init__.py (0 B)
├── 📄 advanced_exporters.py (1.12 KB)
└── 📄 base_exporter.py (2.48 KB)
├── 📁 exports/
├── 📁 modules/
├── 📁 exporters/
└── 📄 file_exporter.py (481 B)
├── 📁 generators/
├── 📄 __init__.py (133 B)
├── 📄 architecture.py (364 B)
├── 📄 flowchart.py (301 B)
└── 📄 sequence.py (267 B)
├── 📁 renderers/
└── 📄 html_renderer.py (1.45 KB)
└── 📁 templates/
└── 📄 library.py (621 B)
├── 📁 output/
├── 📄 ai_20260410_200742.mmd (305 B)
├── 📄 ai_20260410_200932.mmd (322 B)
├── 📄 ai_20260410_200934.mmd (187 B)
├── 📄 ai_20260410_200936.mmd (276 B)
├── 📄 ai_20260410_200939.mmd (413 B)
├── 📄 ai_20260410_200947.mmd (59 B)
├── 📄 ai_20260410_201145.mmd (230 B)
├── 📄 ai_20260410_201146.mmd (347 B)
├── 📄 ai_20260410_201147.mmd (318 B)
├── 📄 ai_20260410_201320.mmd (213 B)
├── 📄 ai_20260410_201321.mmd (180 B)
├── 📄 ai_20260410_201322.mmd (175 B)
├── 📄 ai_flowchart_20260410_200629.mmd (1.01 KB)
├── 📄 architecture_20260410_191009.mmd (266 B)
├── 📄 architecture_20260410_191231.mmd (415 B)
├── 📄 architecture_20260410_191357.mmd (310 B)
├── 📄 architecture_20260410_191520.mmd (162 B)
├── 📄 custom_20260410_200941.mmd (326 B)
├── 📄 decision_20260410_200920.mmd (133 B)
├── 📄 diagram_20260410_194742.html (4.37 KB)
├── 📄 diagram_20260410_195340.mmd (200 B)
├── 📄 flowchart_20260410_190726.mermaid (1.46 KB)
├── 📄 flowchart_20260410_191230.mmd (533 B)
├── 📄 flowchart_20260410_191356.mmd (664 B)
├── 📄 flowchart_20260410_191519.mmd (204 B)
├── 📄 flowchart_20260410_191741.mmd (888 B)
├── 📄 flowchart_20260410_192109.md (1.85 KB)
├── 📄 flowchart_20260410_192109.mmd (1.75 KB)
├── 📄 flowchart_20260410_192216.mmd (640 B)
├── 📄 flowchart_20260410_192316.mmd (147 B)
├── 📄 flowchart_20260410_193959.mmd (343 B)
├── 📄 flowchart_20260410_194041.mmd (190 B)
├── 📄 flowchart_20260410_194126.mmd (55 B)
├── 📄 flowchart_20260410_194415.mmd (188 B)
├── 📄 flowchart_20260410_194452.mmd (160 B)
├── 📄 flowchart_20260410_194539.mmd (144 B)
├── 📄 flowchart_20260410_194742.mmd (267 B)
├── 📄 formatters.py (705 B)
├── 📄 gantt_20260410_191010.mmd (225 B)
├── 📄 gantt_20260410_191233.mmd (832 B)
├── 📄 gantt_20260410_200923.mmd (102 B)
├── 📄 gantt_20260410_201550.mmd (224 B)
├── 📄 login_20260410_194912.mmd (130 B)
├── 📄 login_20260410_195000.mmd (194 B)
├── 📄 login_20260410_195047.mmd (206 B)
├── 📄 login_20260410_195139.mmd (161 B)
├── 📄 login_20260410_200204.mmd (161 B)
├── 📄 login_20260410_200743.mmd (161 B)
├── 📄 login_20260410_200918.mmd (161 B)
├── 📄 login_20260410_201441.mmd (161 B)
├── 📄 sequence_20260410_190727.mmd (1.03 KB)
├── 📄 sequence_20260410_200926.mmd (119 B)
├── 📄 simple_20260410_200929.mmd (31 B)
├── 📄 simple_20260410_200945.mmd (31 B)
└── 📄 state_20260410_191011.mmd (748 B)
├── 📁 providers/
└── 📄 __init__.py (36 B)
├── 📁 templates/
├── 📄 __init__.py (0 B)
└── 📄 library.py (1.51 KB)
├── 📁 utils/
└── 📄 __init__.py (32 B)
├── 📁 viewer/
├── 📄 __init__.py (0 B)
├── 📄 advanced_viewer.py (1.57 KB)
├── 📄 diagram_viewer.py (7.88 KB)
├── 📄 popup_viewer.py (3.31 KB)
└── 📄 save_handler.py (1.26 KB)
├── 📄 flowclaw.py (11.43 KB)
├── 📄 flowclaw_complete.py (16.77 KB)
├── 📄 flowclaw_enhanced.py (3.14 KB)
├── 📄 flowclaw_final.py (3.16 KB)
├── 📄 flowclaw_fixed.py (6.59 KB)
├── 📄 flowclaw_mermaid_style.py (2.58 KB)
├── 📄 flowclaw_modular.py (2.56 KB)
├── 📄 flowclaw_offline.py (5.92 KB)
├── 📄 flowclaw_simple.py (3.79 KB)
├── 📄 flowclaw_standalone.py (5.37 KB)
├── 📄 flowclaw_viewer.py (14.09 KB)
├── 📄 flowclaw_working.py (4.05 KB)
├── 📄 flowclaw_working_final.py (4.89 KB)
└── 📄 schemaclaw.py (2.96 KB)
├── 📁 fork/
└── 📄 fork.py (932 B)
├── 📁 interpretclaw/
├── 📁 cli/
├── 📄 __init__.py (65 B)
└── 📄 parser.py (162 B)
├── 📁 commands/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (168 B)
└── 📄 translate.cpython-312.pyc (1.57 KB)
├── 📄 __init__.py (30 B)
├── 📄 detect.py (921 B)
├── 📄 help.py (747 B)
├── 📄 languages.py (526 B)
├── 📄 lesson.py (1.04 KB)
├── 📄 listen.py (1.16 KB)
├── 📄 quit.py (74 B)
├── 📄 speak.py (679 B)
├── 📄 translate.py (1.16 KB)
├── 📄 translatedoc.py (1.43 KB)
└── 📄 vocab.py (924 B)
├── 📁 core/
├── 📄 __init__.py (63 B)
├── 📄 config.py (1.3 KB)
└── 📄 data.py (183 B)
├── 📁 references/
├── 📁 asian_languages/
└── 📄 README.md (312 B)
├── 📁 cultural_notes/
└── 📄 README.md (310 B)
├── 📁 european_languages/
└── 📄 README.md (318 B)
├── 📁 grammar/
└── 📄 README.md (296 B)
├── 📁 localization/
└── 📄 README.md (306 B)
├── 📁 middle_eastern/
└── 📄 README.md (310 B)
├── 📁 phrase_dictionaries/
└── 📄 README.md (320 B)
└── 📁 translation_apis/
└── 📄 README.md (314 B)
├── 📁 translator/
├── 📁 engines/
├── 📄 __init__.py (245 B)
├── 📄 base.py (562 B)
├── 📄 simple_engine.py (1.31 KB)
└── 📄 webclaw_engine.py (1.33 KB)
├── 📁 formats/
├── 📄 __init__.py (279 B)
├── 📄 base.py (612 B)
├── 📄 docx_format.py (1.42 KB)
├── 📄 markdown_format.py (1.27 KB)
└── 📄 text_format.py (814 B)
├── 📄 __init__.py (375 B)
├── 📄 core.py (2.88 KB)
└── 📄 llm_translator.py (634 B)
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
└── 📄 interpretclaw.py (2.43 KB)
├── 📁 langclaw/
├── 📁 audio/
├── 📁 stt/
├── 📁 providers/
└── 📄 google_stt.py (768 B)
├── 📄 engine.py (665 B)
└── 📄 recorder.py (1.22 KB)
├── 📁 tts/
├── 📁 providers/
├── 📄 edge_tts.py (1.34 KB)
├── 📄 google_tts.py (1.1 KB)
└── 📄 system_tts.py (915 B)
├── 📄 engine.py (1.21 KB)
└── 📄 player.py (3.64 KB)
├── 📄 stt_engine.py (5.22 KB)
└── 📄 tts_engine.py (4.8 KB)
├── 📁 cli/
├── 📄 __init__.py (30 B)
└── 📄 interface.py (4.04 KB)
├── 📁 commands/
├── 📄 __init__.py (25 B)
├── 📄 commands.py (478 B)
├── 📄 conversation.py (823 B)
├── 📄 lesson.py (779 B)
├── 📄 practice.py (662 B)
├── 📄 speak.py (321 B)
├── 📄 teach.py (753 B)
└── 📄 vocab.py (829 B)
├── 📁 config/
├── 📄 __init__.py (33 B)
└── 📄 settings.py (1.08 KB)
├── 📁 core/
├── 📄 __init__.py (31 B)
├── 📄 agent.py (1.32 KB)
├── 📄 lesson_engine.py (1.8 KB)
├── 📄 llm_wrapper.py (1.18 KB)
├── 📄 session_manager.py (980 B)
├── 📄 stt_engine.py (2.2 KB)
├── 📄 translator.py (1.47 KB)
└── 📄 tts_engine.py (2.16 KB)
├── 📁 fetchers/
├── 📄 __init__.py (35 B)
├── 📄 translation_fetcher.py (1.2 KB)
└── 📄 url_fetcher.py (995 B)
├── 📁 providers/
├── 📄 __init__.py (36 B)
├── 📄 api_provider.py (1.96 KB)
└── 📄 webclaw_provider.py (2.94 KB)
├── 📁 references/
├── 📁 asian_languages/
└── 📄 README.md (312 B)
├── 📁 cultural_notes/
└── 📄 README.md (310 B)
├── 📁 european_languages/
└── 📄 README.md (318 B)
├── 📁 grammar/
└── 📄 README.md (296 B)
├── 📁 localization/
└── 📄 README.md (306 B)
├── 📁 middle_eastern/
└── 📄 README.md (310 B)
├── 📁 phrase_dictionaries/
└── 📄 README.md (320 B)
├── 📁 translation_apis/
└── 📄 README.md (314 B)
├── 📄 __init__.py (37 B)
└── 📄 languages.md (1.22 KB)
├── 📁 stt/
└── 📄 stt_engine.py (5.22 KB)
├── 📁 teacher/
├── 📁 lessons/
└── 📁 es/
└── 📄 greetings_beginner.md (569 B)
└── 📄 core.py (2.34 KB)
├── 📁 tts/
├── 📁 providers/
├── 📄 edge_tts.py (1.34 KB)
├── 📄 google_tts.py (1.1 KB)
└── 📄 system_tts.py (915 B)
├── 📄 engine.py (1.21 KB)
├── 📄 player.py (3.64 KB)
└── 📄 tts_engine.py (4.8 KB)
├── 📁 tts_cache/
├── 📄 google_es_682302535184967994.mp3 (6 KB)
├── 📄 google_es_-6837574656301321503.mp3 (6 KB)
├── 📄 google_es_7298730963098077579.mp3 (6 KB)
└── 📄 google_es_-7505699946232858754.mp3 (6 KB)
├── 📁 utils/
├── 📄 __init__.py (32 B)
└── 📄 helpers.py (731 B)
├── 📄 __init__.py (48 B)
├── 📄 langclaw.py (2.79 KB)
├── 📄 test_audio.py (451 B)
└── 📄 test_player.py (473 B)
├── 📁 langclaw_backup/
├── 📁 cli/
├── 📄 __init__.py (65 B)
└── 📄 parser.py (162 B)
├── 📁 commands/
├── 📄 __init__.py (123 B)
└── 📄 system.py (345 B)
├── 📁 core/
├── 📄 __init__.py (63 B)
└── 📄 data.py (181 B)
├── 📁 references/
├── 📁 resources/
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
└── 📄 langclaw.py (1.47 KB)
├── 📁 lawclaw/
├── 📁 __pycache__/
└── 📄 agent_handler.cpython-312.pyc (3.29 KB)
├── 📁 _archive/
├── 📁 display/
├── 📁 file/
├── 📄 __init__.py (0 B)
└── 📄 markdown_exporter.py (1 KB)
├── 📁 index/
├── 📄 __init__.py (0 B)
└── 📄 chronicle_indexer.py (1.74 KB)
├── 📁 web/
├── 📄 __init__.py (0 B)
└── 📄 html_generator.py (4.68 KB)
├── 📄 __init__.py (0 B)
└── 📄 court_orchestrator.py (5.01 KB)
├── 📁 queries/
├── 📄 __init__.py (53 B)
└── 📄 webclaw_queries.py (1.2 KB)
├── 📁 synthesis/
├── 📄 __init__.py (48 B)
└── 📄 llm_synthesis.py (3.86 KB)
├── 📄 create_commands.ps1 (939 B)
├── 📄 lawclaw_backup.py (8.31 KB)
└── 📄 lawclaw_original.py (21.62 KB)
├── 📁 cli/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (232 B)
└── 📄 parser.cpython-312.pyc (676 B)
├── 📄 __init__.py (67 B)
└── 📄 parser.py (329 B)
├── 📁 commands/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (2.21 KB)
├── 📄 analyze.cpython-312.pyc (2.16 KB)
├── 📄 ask.cpython-312.pyc (1.48 KB)
├── 📄 brief.cpython-312.pyc (819 B)
├── 📄 browse.cpython-312.pyc (2.11 KB)
├── 📄 cinfo.cpython-312.pyc (1.45 KB)
├── 📄 cite.cpython-312.pyc (952 B)
├── 📄 court.cpython-312.pyc (2.27 KB)
├── 📄 docket.cpython-312.pyc (812 B)
├── 📄 federal.cpython-312.pyc (887 B)
├── 📄 judge.cpython-312.pyc (893 B)
├── 📄 jurisdiction.cpython-312.pyc (1.06 KB)
├── 📄 law.cpython-312.pyc (428 B)
├── 📄 list.cpython-312.pyc (1.73 KB)
├── 📄 oral.cpython-312.pyc (884 B)
├── 📄 precedent.cpython-312.pyc (931 B)
├── 📄 search.cpython-312.pyc (2.6 KB)
├── 📄 state.cpython-312.pyc (1.36 KB)
├── 📄 stats.cpython-312.pyc (2.37 KB)
├── 📄 statute.cpython-312.pyc (878 B)
└── 📄 summarize.cpython-312.pyc (853 B)
├── 📄 __init__.py (1.46 KB)
├── 📄 analyze.py (1.68 KB)
├── 📄 ask.py (1.02 KB)
├── 📄 brief.py (366 B)
├── 📄 browse.py (1.17 KB)
├── 📄 cite.py (473 B)
├── 📄 court.py (1.62 KB)
├── 📄 court.py.backup (3.61 KB)
├── 📄 docket.py (358 B)
├── 📄 federal.py (461 B)
├── 📄 judge.py (427 B)
├── 📄 jurisdiction.py (651 B)
├── 📄 law.py (197 B)
├── 📄 list.py (940 B)
├── 📄 oral.py (418 B)
├── 📄 precedent.py (460 B)
├── 📄 search.py (1.72 KB)
├── 📄 state.py (743 B)
├── 📄 stats.py (1.17 KB)
├── 📄 statute.py (410 B)
└── 📄 summarize.py (397 B)
├── 📁 core/
├── 📄 __init__.py (384 B)
├── 📄 agent.py (385 B)
├── 📄 api.py (1.77 KB)
├── 📄 app.py (1.38 KB)
├── 📄 app.py.backup (4.4 KB)
├── 📄 config.py (610 B)
├── 📄 data.py (1.92 KB)
└── 📄 display.py (1.11 KB)
├── 📁 law_search/
├── 📄 case_searcher.py (3.51 KB)
└── 📄 llm_searcher.py (2.07 KB)
├── 📁 utils/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (322 B)
└── 📄 display.cpython-312.pyc (4.06 KB)
├── 📄 __init__.py (168 B)
├── 📄 display.py (1.98 KB)
└── 📄 helpers.py (257 B)
├── 📄 agent_handler.py (2.5 KB)
└── 📄 lawclaw.py (3.33 KB)
├── 📁 liberateclaw/
├── 📁 cli/
└── 📄 __init__.py (0 B)
├── 📁 commands/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (167 B)
├── 📄 liberated.cpython-312.pyc (1.63 KB)
└── 📄 models.cpython-312.pyc (1.2 KB)
├── 📄 __init__.py (0 B)
├── 📄 liberate.py (1.53 KB)
├── 📄 liberated.py (1 KB)
├── 📄 models.py (760 B)
├── 📄 obliterate.py (1.95 KB)
├── 📄 remote.py (3.79 KB)
└── 📄 use.py (1.53 KB)
├── 📁 config/
└── 📄 __init__.py (0 B)
├── 📁 core/
└── 📄 __init__.py (0 B)
├── 📁 data/
└── 📄 shared_memory.json (109 B)
├── 📁 exports/
├── 📄 codellama-liberated.Modelfile (373 B)
├── 📄 deepseek-coder-liberated.Modelfile (380 B)
├── 📄 deepseek-r1-liberated.Modelfile (375 B)
├── 📄 gemma3-liberated.Modelfile (370 B)
├── 📄 llama3.2-liberated.Modelfile (372 B)
├── 📄 qwen3-coder-liberated.Modelfile (376 B)
└── 📄 qwen3-vl-liberated.Modelfile (373 B)
├── 📁 fetchers/
└── 📄 __init__.py (0 B)
├── 📁 providers/
└── 📄 __init__.py (0 B)
├── 📁 utils/
└── 📄 __init__.py (0 B)
└── 📄 liberateclaw.py (4.2 KB)
├── 📁 llmclaw/
├── 📁 __pycache__/
└── 📄 agent_handler.cpython-312.pyc (1.79 KB)
├── 📁 cli/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (157 B)
└── 📄 interface.cpython-312.pyc (4.05 KB)
├── 📄 __init__.py (0 B)
└── 📄 interface.py (2.74 KB)
├── 📁 commands/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (387 B)
├── 📄 ask.cpython-312.pyc (4.15 KB)
├── 📄 list.cpython-312.pyc (2.58 KB)
├── 📄 llm.cpython-312.pyc (4.73 KB)
├── 📄 llm_backup.cpython-312.pyc (4.15 KB)
├── 📄 llm_enhanced.cpython-312.pyc (4.74 KB)
├── 📄 llm_smart.cpython-312.pyc (1.94 KB)
├── 📄 normal.cpython-312.pyc (1.21 KB)
├── 📄 obliterated.cpython-312.pyc (1.69 KB)
└── 📄 use.cpython-312.pyc (1.67 KB)
├── 📄 __init__.py (231 B)
├── 📄 list.py (1.45 KB)
├── 📄 llm.py (3.38 KB)
├── 📄 llm_backup.py (2.8 KB)
├── 📄 llm_enhanced.py (3.38 KB)
├── 📄 llm_smart.py (1.74 KB)
├── 📄 normal.py (580 B)
├── 📄 obliterated.py (773 B)
└── 📄 use.py (1.13 KB)
├── 📁 core/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (158 B)
├── 📄 state.cpython-312.pyc (1.85 KB)
└── 📄 sync.cpython-312.pyc (3.05 KB)
├── 📄 __init__.py (0 B)
├── 📄 state.py (1.07 KB)
└── 📄 sync.py (2.33 KB)
├── 📁 providers/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (163 B)
├── 📄 obliterated.cpython-312.pyc (5.85 KB)
└── 📄 stock.cpython-312.pyc (5.05 KB)
├── 📄 __init__.py (0 B)
├── 📄 obliterated.py (3.67 KB)
└── 📄 stock.py (3.01 KB)
├── 📁 utils/
└── 📄 __init__.py (0 B)
├── 📄 agent_handler.py (1.15 KB)
└── 📄 llmclaw.py (1.09 KB)
├── 📁 mathematicaclaw/
├── 📁 cli/
├── 📄 __init__.py (65 B)
├── 📄 interface.py (7.76 KB)
├── 📄 main.py (5.82 KB)
└── 📄 parser.py (162 B)
├── 📁 commands/
├── 📄 __init__.py (32 B)
├── 📄 add.py (182 B)
├── 📄 algebra.py (2.24 KB)
├── 📄 arithmetic.py (2.45 KB)
├── 📄 calculus.py (1.4 KB)
├── 📄 math.py (3.91 KB)
├── 📄 plot.py (932 B)
├── 📄 solve.py (436 B)
└── 📄 system.py (370 B)
├── 📁 config/
└── 📄 settings.py (221 B)
├── 📁 core/
├── 📄 __init__.py (0 B)
├── 📄 agent.py (2.25 KB)
├── 📄 data.py (188 B)
├── 📄 engine.py (7.58 KB)
├── 📄 math_engine.py (4.25 KB)
└── 📄 session_manager.py (795 B)
├── 📁 data/
└── 📄 shared_memory.json (113 B)
├── 📁 handlers/
├── 📄 __init__.py (185 B)
├── 📄 algebra.py (840 B)
├── 📄 algebra_commands.py (2.57 KB)
├── 📄 arithmetic_commands.py (3.13 KB)
├── 📄 calculus.py (532 B)
├── 📄 calculus_commands.py (1.86 KB)
├── 📄 command_handler.py (1.97 KB)
├── 📄 expression_handler.py (470 B)
├── 📄 math_handler.py (1.01 KB)
├── 📄 plot_commands.py (1.54 KB)
├── 📄 plotting.py (971 B)
└── 📄 system_commands.py (685 B)
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
├── 📁 visualization/
├── 📄 __init__.py (160 B)
├── 📄 graph_builder.py (3.62 KB)
└── 📄 plotter.py (5.75 KB)
├── 📄 __init__.py (152 B)
├── 📄 agent.py (4.24 KB)
├── 📄 ai_assistant.py (12.42 KB)
├── 📄 ai_visualizer.py (2.36 KB)
├── 📄 mathematicaclaw.py (2.11 KB)
└── 📄 mathematicaclaw_complete.py (6.18 KB)
├── 📁 mediclaw/
├── 📁 cli/
├── 📄 __init__.py (1.76 KB)
└── 📄 interface.py (7.83 KB)
├── 📁 commands/
├── 📄 __init__.py (25 B)
├── 📄 base.py (239 B)
├── 📄 clinical_commands.py (1.01 KB)
├── 📄 commands.py (7.65 KB)
├── 📄 core_commands.py (1.42 KB)
├── 📄 diagnose.py (321 B)
├── 📄 lifestyle_commands.py (1.29 KB)
├── 📄 med.py (966 B)
├── 📄 pharma_commands.py (984 B)
├── 📄 research.py (629 B)
├── 📄 sources.py (518 B)
├── 📄 specialty_commands.py (1.21 KB)
├── 📄 stats.py (441 B)
└── 📄 treatment.py (327 B)
├── 📁 config/
└── 📄 settings.py (1000 B)
├── 📁 core/
├── 📄 agent.py (387 B)
└── 📄 engine.py (1.25 KB)
├── 📁 docs/
└── 📄 Mediclaw.md (11.42 KB)
├── 📁 fetchers/
└── 📄 url_fetcher.py (1.94 KB)
├── 📁 providers/
├── 📄 __init__.py (1.5 KB)
├── 📄 anthropic.py (1.01 KB)
├── 📄 api_provider.py (1.25 KB)
├── 📄 base.py (253 B)
├── 📄 ollama.py (970 B)
├── 📄 ollama_provider.py (836 B)
├── 📄 openrouter.py (835 B)
├── 📄 openrouter_provider.py (917 B)
├── 📄 providers.py (2.43 KB)
└── 📄 webclaw_provider.py (853 B)
├── 📁 utils/
├── 📄 __init__.py (88 B)
└── 📄 helpers.py (255 B)
└── 📄 mediclaw.py (1.58 KB)
├── 📁 plotclaw/
├── 📁 cli/
└── 📄 __init__.py (30 B)
├── 📁 commands/
├── 📄 bar.py (1.61 KB)
├── 📄 pie.py (1.39 KB)
└── 📄 plot.py (1.89 KB)
├── 📁 core/
├── 📄 __init__.py (31 B)
└── 📄 agent.py (1.52 KB)
├── 📁 exports/
├── 📄 bar_2646.png (23.18 KB)
├── 📄 pie_1317.png (33.26 KB)
├── 📄 plot_153.png (64.95 KB)
└── 📄 plot_4417.png (53.67 KB)
├── 📁 providers/
└── 📄 __init__.py (36 B)
├── 📁 utils/
└── 📄 __init__.py (32 B)
├── 📄 plotclaw.py (1.7 KB)
└── 📄 utils.py (301 B)
├── 📁 rustypycraw/
├── 📁 a2a/
├── 📄 __init__.py (0 B)
└── 📄 client.py (1.67 KB)
├── 📁 integrations/
└── 📄 chronicle_bridge.py (5.54 KB)
├── 📁 modules/
├── 📁 analyzer/
├── 📄 __init__.py (41 B)
└── 📄 code_analyzer.py (170 B)
├── 📁 crawler/
├── 📄 __init__.py (37 B)
└── 📄 ast_crawler.py (65 B)
├── 📁 indexer/
├── 📄 __init__.py (49 B)
└── 📄 chronicle_indexer.py (162 B)
├── 📁 llm/
├── 📄 __init__.py (37 B)
└── 📄 groq_client.py (114 B)
├── 📁 scanner/
├── 📄 __init__.py (39 B)
└── 📄 code_scanner.py (124 B)
└── 📄 __init__.py (27 B)
└── 📄 rustypycraw.py (1.03 KB)
├── 📁 shared/
├── 📁 __pycache__/
├── 📄 a2a_client.cpython-312.pyc (3.14 KB)
└── 📄 base_agent.cpython-312.pyc (2.71 KB)
├── 📁 collaboration/
└── 📄 agent_bridge.py (2.25 KB)
├── 📁 importers/
└── 📄 unified_importer.py (9.88 KB)
├── 📁 memory/
├── 📄 procedural_memory.py (5.23 KB)
└── 📄 three_tier.py (5.28 KB)
├── 📁 safety/
├── 📄 __init__.py (112 B)
└── 📄 trauma_guard.py (1.83 KB)
├── 📄 a2a_client.py (2.28 KB)
├── 📄 acp_client.py (2.15 KB)
├── 📄 agent_loader.py (1.64 KB)
├── 📄 base_agent.py (1.37 KB)
├── 📄 base_agent_enhanced.py (1.54 KB)
├── 📄 budget_controller.py (2.78 KB)
├── 📄 chronicle_integration.py (1.18 KB)
├── 📄 decomposer.py (3.27 KB)
├── 📄 mcp_registry.py (3.99 KB)
├── 📄 router.py (3.47 KB)
└── 📄 sandbox.py (2.33 KB)
├── 📁 TXclaw/
├── 📁 .txclaw/
└── 📄 networks.json (547 B)
├── 📁 cli/
├── 📄 commands_list.py (2.62 KB)
└── 📄 interface.py (3.86 KB)
├── 📁 commands/
└── 📄 __init__.py (23 B)
├── 📁 config/
└── 📄 settings.py (997 B)
├── 📁 contracts/
├── 📁 auction_contract/
├── 📁 src/
└── 📄 contract.rs (3.77 KB)
└── 📄 Cargo.toml (366 B)
└── 📁 my_auction_contract/
├── 📁 src/
└── 📄 contract.rs (4.66 KB)
└── 📄 Cargo.toml (369 B)
├── 📁 core/
├── 📄 agent.py (568 B)
└── 📄 commands.py (3.57 KB)
├── 📁 fetchers/
└── 📄 url_fetcher.py (2.41 KB)
├── 📁 modules/
├── 📁 ai/
├── 📄 __init__.py (38 B)
└── 📄 assistant.py (243 B)
├── 📁 contracts/
├── 📄 __init__.py (42 B)
└── 📄 generator.py (227 B)
├── 📁 deploy/
├── 📄 __init__.py (36 B)
└── 📄 handler.py (228 B)
├── 📁 network/
├── 📄 __init__.py (37 B)
└── 📄 handler.py (214 B)
├── 📁 references/
├── 📄 __init__.py (39 B)
└── 📄 handler.py (208 B)
├── 📁 tests/
├── 📄 __init__.py (38 B)
└── 📄 generator.py (229 B)
└── 📄 __init__.py (22 B)
├── 📁 providers/
└── 📄 api_provider.py (1.58 KB)
├── 📁 references/
└── 📄 tx_references.py (1.65 KB)
├── 📁 utils/
└── 📄 helpers.py (1.51 KB)
├── 📄 README.md (1.17 KB)
└── 📄 txclaw.py (1.14 KB)
└── 📁 webclaw/
├── 📁 __pycache__/
├── 📄 agent_handler.cpython-312.pyc (1.26 KB)
├── 📄 api_server.cpython-312.pyc (1.64 KB)
└── 📄 webclaw.cpython-312.pyc (4.35 KB)
├── 📁 a2a/
├── 📄 integrated_server.py (7.24 KB)
└── 📄 search_handler.py (0 B)
├── 📁 cache/
├── 📄 url_index.json (3.68 MB)
├── 📄 web_cache.db (280.17 MB)
└── 📄 webclaw_references.pkl (363.31 MB)
├── 📁 cli/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (272 B)
└── 📄 parser.cpython-312.pyc (645 B)
├── 📄 __init__.py (97 B)
└── 📄 parser.py (251 B)
├── 📁 commands/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (1.2 KB)
├── 📄 browse.cpython-312.pyc (1.51 KB)
├── 📄 cache_stats.cpython-312.pyc (1.68 KB)
├── 📄 chronicle.cpython-312.pyc (2.25 KB)
├── 📄 fetch.cpython-312.pyc (8.17 KB)
├── 📄 help.cpython-312.pyc (1.58 KB)
├── 📄 list.cpython-312.pyc (1.29 KB)
├── 📄 llm.cpython-312.pyc (2.05 KB)
├── 📄 quit.cpython-312.pyc (420 B)
├── 📄 recall.cpython-312.pyc (1.3 KB)
├── 📄 share.cpython-312.pyc (2.75 KB)
├── 📄 stats.cpython-312.pyc (1.33 KB)
└── 📄 system.cpython-312.pyc (964 B)
├── 📄 __init__.py (990 B)
├── 📄 browse.py (955 B)
├── 📄 cache_stats.py (915 B)
├── 📄 chronicle.py (1.54 KB)
├── 📄 fetch.py (6.74 KB)
├── 📄 help.py (1.34 KB)
├── 📄 list.py (657 B)
├── 📄 llm.py (1.54 KB)
├── 📄 quit.py (210 B)
├── 📄 recall.py (848 B)
├── 📄 share.py (1.95 KB)
├── 📄 stats.py (713 B)
└── 📄 system.py (392 B)
├── 📁 core/
├── 📁 __pycache__/
├── 📄 __init__.cpython-312.pyc (290 B)
├── 📄 agent.cpython-312.pyc (3.24 KB)
├── 📄 api.cpython-312.pyc (3.99 KB)
├── 📄 cache.cpython-312.pyc (6.23 KB)
├── 📄 chronicle_ledger.cpython-312.pyc (8.31 KB)
├── 📄 config.cpython-312.pyc (1.57 KB)
├── 📄 pacer.cpython-312.pyc (4.4 KB)
└── 📄 rate_limiter.cpython-312.pyc (6.07 KB)
├── 📄 __init__.py (142 B)
├── 📄 agent.py (2.11 KB)
├── 📄 api.py (3.34 KB)
├── 📄 cache.py (4.26 KB)
├── 📄 chronicle_ledger.py (6.46 KB)
├── 📄 config.py (899 B)
├── 📄 data.py (263 B)
├── 📄 pacer.py (3.23 KB)
├── 📄 rate_limiter.py (4.39 KB)
└── 📄 shared_memory.py (3.63 KB)
├── 📁 docs/
└── 📄 webclaw_documentation.md (23.49 KB)
├── 📁 providers/
├── 📁 __pycache__/
└── 📄 webclaw_provider.cpython-312.pyc (4.81 KB)
├── 📄 webclaw_provider.py (3.5 KB)
└── 📄 webclaw_provider_backup.py (2.96 KB)
├── 📁 references/
├── 📁 ai_ml/
└── 📄 ai_ml_references.md (2.94 KB)
├── 📁 apis/
└── 📄 README.md (272 B)
├── 📁 backend/
└── 📄 README.md (278 B)
├── 📁 claw_coder/
├── 📁 angular/
├── 📁 animations/
├── 📁 cli/
├── 📁 components/
├── 📁 dependency_injection/
├── 📁 deployment/
├── 📁 directives/
├── 📁 forms/
├── 📁 getting_started/
├── 📁 http_client/
├── 📁 modules/
├── 📁 overview/
├── 📁 performance/
├── 📁 pipes/

---

## 🤖 COMPLETE AGENT INVENTORY


---

## 🧠 COMPLETE LLM MODEL INVENTORY

| Model | Source | Type | Size | Status |
|-------|--------|------|------|--------|
| deepseek-coder-liberated | ollama | 🔥 Obliterated | 3.8 GB | working |
| codellama-liberated | ollama | 🔥 Obliterated | 3.8 GB | working |
| smollm2-liberated | ollama | 🔥 Obliterated | 3.4 GB | working |
| tinyllama-liberated | ollama | 🔥 Obliterated | 2.2 GB | working |
| gemma3-liberated | ollama | 🔥 Obliterated | 815 MB | working |
| hf.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M | ollama | 📦 Standard | 4.7 GB | working |
| deepseek-coder:6.7b | ollama | 📦 Standard | 3.8 GB | working |
| codellama:7b | ollama | 📦 Standard | 3.8 GB | working |
| tinyllama:1.1b | ollama | 📦 Standard | 637 MB | working |
| gemma3:1b | ollama | 📦 Standard | 815 MB | working |
| gemma3:4b | ollama | 📦 Standard | 3.3 GB | working |
| deepseek-r1:8b | ollama | 📦 Standard | 5.2 GB | working |
| gemma3:12b | ollama | 📦 Standard | 8.1 GB | working |
| gemma3:27b | ollama | 📦 Standard | 17 GB | working |
| qwen3-coder:30b | ollama | 📦 Standard | 18 GB | working |
| qwen3-vl:30b | ollama | 📦 Standard | 19 GB | working |
| claude-3-haiku | anthropic | 📦 Standard |  | working |

---

## 📚 KNOWLEDGE BASE REFERENCE INVENTORY

| Category | Files | Size |
|----------|-------|------|
| ai_ml | 1 | 0 MB |
| apis | 1 | 0 MB |
| backend | 1 | 0 MB |
| claw_coder | 1566 | 34.46 MB |
| cloud | 1 | 0 MB |
| cloud_computing | 1 | 0 MB |
| cybersecurity | 1 | 0 MB |
| databases | 2 | 0 MB |
| devops | 2 | 0 MB |
| docuclaw | 21 | 0.02 MB |
| flowclaw | 20 | 0 MB |
| frontend | 2 | 0 MB |
| game_dev | 1 | 0 MB |
| interpretclaw | 38 | 0.01 MB |
| langclaw | 259 | 0.16 MB |

---

## 🗄️ CHRONICLE SQLITE INDEX

**File:** agents\webclaw\cache\web_cache.db
**Size:** 280.17 MB

| Table | Rows | Purpose |
|-------|------|---------|
| web_cache | 20,211 | Cached reference content |
| search_index | 1,484,984 | Searchable terms |


---

## 🔗 A2A SERVER ENDPOINTS

**Port:** 8766
**URL:** http://127.0.0.1:8766

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /health | Server health + memory stats |
| GET | /v1/agents | List all registered agents |
| GET | /memory/stats | Detailed memory statistics |
| POST | /v1/message/{agent} | Send task to specific agent |

**Registered Agents (21):**
- claw_coder
- crustyclaw
- dataclaw
- designclaw
- docuclaw
- draftclaw
- drawclaw
- dreamclaw
- fileclaw
- flowclaw
- interpretclaw
- langclaw
- langclaw_backup
- lawclaw
- liberateclaw
- llmclaw
- mathematicaclaw
- mediclaw
- plotclaw
- rustypycraw
- TXclaw
- webclaw

---

## 🔧 CORE MODULES

- core\agent_loader.py
- core\command_router.py
- core\llm_manager.py
- core\math_engine.py
- core\permissions.py
- core\query_loop.py
- core\state.py
- core\tool.py
- core\__init__.py
- core\fork\fork_agent.py
- core\llm\cache.py
- core\llm\config.py
- core\llm\manager.py
- core\llm\__init__.py
- core\llm\providers\base.py
- core\llm\providers\factory.py
- core\llm\providers\groq.py
- core\llm\providers\ollama.py
- core\llm\providers\__init__.py
- core\query\loop.py
- core\query\state.py
- core\query\terminal.py
- core\query\__init__.py

---

## 📦 SHARED MODULES

- shared\agent_router.py
- shared\base_agent.py
- shared\batcher.py
- shared\chronicle_helper.py
- shared\commands.py
- shared\compactor.py
- shared\config.py
- shared\edit_tools.py
- shared\error_handler.py
- shared\input_handler.py
- shared\latches.py
- shared\logging.py
- shared\metrics.py
- shared\observability.py
- shared\output_handler.py
- shared\permissions.py
- shared\rate_limiter.py
- shared\router.py
- shared\security.py
- shared\shutdown.py
- shared\validation.py
- shared\__init__.py
- shared\fork\__init__.py
- shared\hooks\hook_manager.py
- shared\hooks\hook_matcher.py
- shared\hooks\hook_types.py
- shared\hooks\__init__.py
- shared\hooks\runners\agent_runner.py
- shared\hooks\runners\command_runner.py
- shared\hooks\runners\http_runner.py
- shared\hooks\runners\prompt_runner.py
- shared\hooks\runners\__init__.py
- shared\llm\anthropic.py
