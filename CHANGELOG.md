# Version v2.0.3beta

## Fixes
* Do not release as draft ([9966c27](https://github.com/Kastakin/PyES/commit/9966c27e5388985a419d99e5d74dadcd3f2d3ae6))

## Chores
* Update deprecated runner ([90c9ddf](https://github.com/Kastakin/PyES/commit/90c9ddfe9eefd211da2e7d50403e3301e43fa210))


# Version v2.0.2beta

## Fixes
* Correctly handle github ref tags ([74e2e3f](https://github.com/Kastakin/PyES/commit/74e2e3fa48ac7023c808a301e37f408642d2d4a5))
* Correctly assign artifact names in release ([28ee8ea](https://github.com/Kastakin/PyES/commit/28ee8eaa8b9e0deb3db92d0b8c701033cab0caad))
* correctly select work mode when importing BSTAC files ([556adbd](https://github.com/Kastakin/PyES/commit/556adbd10a331ad7c625a577d5fe767e7aca3c21))
* Increase number of allowed decimals for titration fields ([64e7c73](https://github.com/Kastakin/PyES/commit/64e7c736ef88a1446bc0e385aea5e1c3acc84bb9))

## Chores
* Update libeq to fix bstac import ([f9ba49c](https://github.com/Kastakin/PyES/commit/f9ba49c878d28f1ac9614071ee81c09046b3f3df))


# Version v2.0.1beta

## Fixes
* Fix regression in opening file from cli argument ([c39cf5a](https://github.com/Kastakin/PyES/commit/c39cf5a332acac2a4de465872e500d82e0e294d3))
* Solve importing and exporting issues of titration data ([8bc5e03](https://github.com/Kastakin/PyES/commit/8bc5e03ae20c3d293fa1fcd752543d67d033f312))

## Chores
* Formatting and import sorting ([43b6bdd](https://github.com/Kastakin/PyES/commit/43b6bdda8c0871e820a0b1508eeb3c261bab2ed5))


# Version v1.1.3

## Features
* Add commands to edit all columns ([7a709ed](https://github.com/Kastakin/PyES/commit/7a709edf0a5c83c3b172933de6e557f67b0b73eb))
* Calculate percentages on the fly for plotting purposes ([ddc04d7](https://github.com/Kastakin/PyES/commit/ddc04d7797c277df9717b15685a5bed684caec06))

## Enhancements
* Use dequeue instead of list for keeping track of concentration of previous points ([b919663](https://github.com/Kastakin/PyES/commit/b919663dd7ebcd712189f1bdcdcf8e86719f629d))

## Fixes
* Update Pillow dependency to avoid vulnerability ([1b72e3c](https://github.com/Kastakin/PyES/commit/1b72e3c00475079db0d03715d7d23ace1fb0fee4))

## Chores
* Add missing generated artifacts ([4ddba12](https://github.com/Kastakin/PyES/commit/4ddba12534f8d17b3150912a705e9e1e7ea3b3d0))
* Lock pyinstaller version ([a9151b5](https://github.com/Kastakin/PyES/commit/a9151b5496bf99eaa9ae98e8abcefd5820a33d19))
* Improve reliability of benchmark scripts ([a9c186b](https://github.com/Kastakin/PyES/commit/a9c186b1b6a1ca8cfe303500f7dc69e37588c71d))
* Add generics methods for models ([d0b61c3](https://github.com/Kastakin/PyES/commit/d0b61c335574592ebca45e2b3da1534e51a8f960))


# Version v1.1.2

## Features
* Add monochrome plots and allow chainging units of volume and concentration ([b1d3db0](https://github.com/Kastakin/PyES/commit/b1d3db09584cbb1368a74c631f49ce2b18bc65bd))

## Enhancements
* Better traceback when in debug mode ([b980e12](https://github.com/Kastakin/PyES/commit/b980e1217287a9823796fdbe6831a3bfa94d6b02))
* Relax pyqtgraph requirements ([9785578](https://github.com/Kastakin/PyES/commit/9785578b1cfe9ed4de38a5db2f771fb0f1179f72))

## Fixes
* Remove titrant concentraions when ignoring comps ([66ec54a](https://github.com/Kastakin/PyES/commit/66ec54ae37b88ac6f07a69730a7d5b020c06e840))


# Version v1.1.1

## Fixes
* Solve bug in export dialog ([3b45584](https://github.com/Kastakin/PyES/commit/3b45584bf14499806c70f28ef8c8f34c6fe2da15))


# Version v1.1.0

## Features
* Add undo for all editable fields ([b9af1d1](https://github.com/Kastakin/PyES/commit/b9af1d1ec8f0087d2be18578f52e023914518d11))

## Enhancements
* Easier plot export ([39a887f](https://github.com/Kastakin/PyES/commit/39a887fb4445ad78926bae82cd30918ca722fd5d))
* Plot error bars for concentrations on plot ([e562ed6](https://github.com/Kastakin/PyES/commit/e562ed698e8c45ddf7156677a1f84c9597ca88f1))
* Aske for confirmation when changing projects ([d70732b](https://github.com/Kastakin/PyES/commit/d70732b891485bda212002a59ca17c1a90c9d095))
* Add undo for compontents models ([0dacdc2](https://github.com/Kastakin/PyES/commit/0dacdc2ded283d135968ed3f889f2e2b6d9fbdda))
* Add info dialogs to inputs ([](https://github.com/Kastakin/PyES/commit/))
* Refactor of models code for undo ([cea0f69](https://github.com/Kastakin/PyES/commit/cea0f69f27bcb13ff99c47d8d487ac4dc31f1410))
* Unify species models and add edit undo ([8d86ae7](https://github.com/Kastakin/PyES/commit/8d86ae7b006c2d9d8f803d671ed85618afc75f93))
* Add undo for tables row swapping ([a84d860](https://github.com/Kastakin/PyES/commit/a84d86055c81feb4b6dee4a72abae004f52f0d01))
*  Add undo for comp tables add/remove ([baa396b](https://github.com/Kastakin/PyES/commit/baa396bf9da5220bb33424211543a9d2603fc432))
* Add undo for species tables add/remove ([d64bef2](https://github.com/Kastakin/PyES/commit/d64bef2b25f6c019e97f05f38d1a465786cc4440))
* Rework opening of files to report errors ([b08fd9c](https://github.com/Kastakin/PyES/commit/b08fd9cc1086335978966f2d935bb87c866f681c))
* simplify rowCount and columnCount methods ([677cee1](https://github.com/Kastakin/PyES/commit/677cee1c572ca3d24cc9ae212bab38d915909a5f))
* Allow opening files directly ([34cb86f](https://github.com/Kastakin/PyES/commit/34cb86fed369453ff3790eb126264ee11c0eebe3))

## Fixes
* Change input labels when ind comp change ([62f8d84](https://github.com/Kastakin/PyES/commit/62f8d840f00f72abcc2b8f2f7a79f3c29f8524ac))
* Workaround empty species header exception ([4a2a2fa](https://github.com/Kastakin/PyES/commit/4a2a2fae00890bc34e6aa70603aaf86bfa1fca29))
* Typos in graph axis title ([718319b](https://github.com/Kastakin/PyES/commit/718319b48188c05832b2a3991ccd030e9fccca64))
* Remove unused comments ([cbeef10](https://github.com/Kastakin/PyES/commit/cbeef10b1602ae1035bedf80eab7d159d9259e83))
* Better handle name of new components ([3871ee8](https://github.com/Kastakin/PyES/commit/3871ee8d4efe767a2b75caebd3174c1f3335efb9))
* Remove debug statement ([98dcc99](https://github.com/Kastakin/PyES/commit/98dcc997d60dc430ab1ea224e4760619198e1c38))
* Update open editor after swapping rows ([4a70434](https://github.com/Kastakin/PyES/commit/4a70434dfbca25f7d81ba18f172e97eba1f698d8))
* Fix tests to account for dialog on close ([5dfdddb](https://github.com/Kastakin/PyES/commit/5dfdddb3b727828e681babf53db1ffd75c3af526))
* Correct components view delegates ([ece92f7](https://github.com/Kastakin/PyES/commit/ece92f7c6a15f505c1856334a446c3999747775c))
* Remove useless about qt dialog call ([527c25f](https://github.com/Kastakin/PyES/commit/527c25f1b9ae2099afe04835c9c8939ad69356c2))
* Rewrite delegate init ([ae21b84](https://github.com/Kastakin/PyES/commit/ae21b84c9b61a5413659fe2193e8fd442e8a8060))
* Simplify species actions ([fdc5f13](https://github.com/Kastakin/PyES/commit/fdc5f13b1bbf24657cb185e028e6352486cec510))
* Remove unneeded check for species model ([f8ec329](https://github.com/Kastakin/PyES/commit/f8ec3292ffcbce255210e0bed754be6344ee0f67))
* Handle files empty dataframes for solids ([07d8d0a](https://github.com/Kastakin/PyES/commit/07d8d0ae3b65d14b6893609205ad4dcf96f6da90))

## Chores
* Calrify enums coming from Qt ([ce5d64a](https://github.com/Kastakin/PyES/commit/ce5d64a8df908a47899331b0e993f53430819a0a))
* Remove debug statements ([2605e81](https://github.com/Kastakin/PyES/commit/2605e8182a218092e825fc9283ca0adba9bf14d0))
* Fix imports ([4719a01](https://github.com/Kastakin/PyES/commit/4719a01d429470689d4a14d834e6b4e458fcb106))


# Version v1.0.0

## Enhancements
* Rename errors uncertainty to avoid confusion ([de71680](https://github.com/Kastakin/PyES/commit/de716806790828cc94fb42495e5c13a3e1933e07))
* Add user manual (pdf from latex) ([9276abe](https://github.com/Kastakin/PyES/commit/9276abede5912f496c720d9d2d0bb43d0a088919))

## Chores
* update pre-commit ([1c180a0](https://github.com/Kastakin/PyES/commit/1c180a0924b4bc50718812be48601f0b4eb17083))


# Version v0.4.4

## Enhancements
* Add AboutQt dialog for LGPL compliance ([0ab1b8b](https://github.com/Kastakin/PyES/commit/0ab1b8b9eca07100409f55c44988de9c66925613))
* Create log folder in home at runtime ([6c9cdeb](https://github.com/Kastakin/PyES/commit/6c9cdebe0bc4b39bde0663f77e57612a196db827))
* Simplify Components tests ([a81990c](https://github.com/Kastakin/PyES/commit/a81990c04c086a9583dc12a9123aae6bb6eab269))
* GUI test handle interface pytest fixture ([9de8c43](https://github.com/Kastakin/PyES/commit/9de8c43d38d9f42eacc6d2b92c98605a631b663c))

## Fixes
* Fix paths in tbump config ([956f458](https://github.com/Kastakin/PyES/commit/956f4589301189c4293abbda09626f2b63e111d0))
* Remove top level init for PyInstaller ([f27946b](https://github.com/Kastakin/PyES/commit/f27946b778644be30df8202a0b53499445563966))
* Regression bugs in optimizer ([](https://github.com/Kastakin/PyES/commit/))
* Use correct es4 data for cu_gly test system ([97930aa](https://github.com/Kastakin/PyES/commit/97930aa43df60cc32260c2fdf3d6ba3bce7ed0ec))
* Handle displayed tables better ([0c8e08d](https://github.com/Kastakin/PyES/commit/0c8e08db037ae8949c26cf747c488bf8a01acb27))
* Update path for benchmark script ([7cd17d6](https://github.com/Kastakin/PyES/commit/7cd17d6f31903bef8c290fbc3a0a493f0fcdf8e6))
* Change resource file location ([5a3f915](https://github.com/Kastakin/PyES/commit/5a3f915e6cced2e36b29c57d84858d55dbecda77))
* Correct the test file for HySS comparison ([ef5aa58](https://github.com/Kastakin/PyES/commit/ef5aa584e042219298e4122ac0d606801ec8c37a))
* Adding component last now works as intended ([8f75480](https://github.com/Kastakin/PyES/commit/8f75480cea3f7d84c28c509ebd7506e1100c6cc5))

## Chores
* Fix files and exceptions for tests ([2ae3b40](https://github.com/Kastakin/PyES/commit/2ae3b4022c7982386c1bbda79f94487c922c4d6b))
* Add resource_rc to coverage exceptions ([96683f6](https://github.com/Kastakin/PyES/commit/96683f63d44e8de47a8313721d73059e0689d534))
* Better coverage settings handling ([e1c5d48](https://github.com/Kastakin/PyES/commit/e1c5d48493954915249aeb7ea005d182bd4bf0f4))
* Add tests for solids in cu-gly system ([4a86b25](https://github.com/Kastakin/PyES/commit/4a86b255952e1a3a9d1e26b42752c6c6b07c7114))
* Format JSON files ([5d0e96a](https://github.com/Kastakin/PyES/commit/5d0e96a715b106202bc3bd76278248f9d35e76a7))
* Add Json formatter to hooks ([1bbc02f](https://github.com/Kastakin/PyES/commit/1bbc02f1378d491fc4b2a02c602d19392bbbdcf6))
* Add test suit ([7326aa2](https://github.com/Kastakin/PyES/commit/7326aa268c52f9d7d2b904acf7b1997a211819bb))


# Version v0.4.3

## Enhancements
* Better colors for darkmode ([c0150af](https://github.com/Kastakin/PyES/commit/c0150afd7a0189594b6fa6fd23d9e0c622190ff0))

## Chores
* Update release creation options for CI ([094b04c](https://github.com/Kastakin/PyES/commit/094b04c211c44be5ec9eeff4ae38dbd55e18fde1))
* Bump requirements (PySide6.4) ([8015b99](https://github.com/Kastakin/PyES/commit/8015b99612d458c72fc60c8a07e61b00fb64cb8c))


# Version v0.4.2

## Features
* Allow change colors in plots ([49610dc](https://github.com/Kastakin/PyES/commit/49610dc3464a39bad4b0c97ebb1318c6ac11d01f))

## Enhancements
* Add example README ([6912940](https://github.com/Kastakin/PyES/commit/6912940055a643cba06fc8208fa24713390ca0e8))
* Preserve indipendent component when switching comp order ([deb32f1](https://github.com/Kastakin/PyES/commit/deb32f146b11644b327148c61a39c649f5080dae))
* Square color pickers in plot window ([16cbfa2](https://github.com/Kastakin/PyES/commit/16cbfa2363ab5bd5b2dfa777ce41afd99bf9aa85))

## Fixes
* Adjust flags behaviour for qt6.4 ([9d5d86a](https://github.com/Kastakin/PyES/commit/9d5d86afb602da3e96eb446d85524605641ec18b))
* Remove unused imports dangling ([b97b7e1](https://github.com/Kastakin/PyES/commit/b97b7e199dfe5e16074c6c47cd37318cfde2658f))
* Avoid recalculating species names in calculation routine ([8f25118](https://github.com/Kastakin/PyES/commit/8f25118545d54615f3057f938f871a29847a7f66))
* Correct error computation of solids ([01db4f2](https://github.com/Kastakin/PyES/commit/01db4f27402dee21fa5df002aae394575059d80e))
* Rename variable for consistency ([31bb88e](https://github.com/Kastakin/PyES/commit/31bb88eea964654bc4137ffa94652aada2062a38))
* Remove unused code ([04d2b54](https://github.com/Kastakin/PyES/commit/04d2b54310b73dd89908d9d23e290ddfd7ca595b))
* Relax damping routine convergence ([26922a5](https://github.com/Kastakin/PyES/commit/26922a56bc99548a3320a54dd2280c796337afe2))

## Chores
* Rollback due to incorrect CI ([707a4e4](https://github.com/Kastakin/PyES/commit/707a4e4cf59045eaaf0b75d87e626dc95e2afbd7))
* Bump requirements ([3d45733](https://github.com/Kastakin/PyES/commit/3d457336464f3e7bb2d8568976ca536c4de82edc))
* Update release workflow ([784fe30](https://github.com/Kastakin/PyES/commit/784fe30f39dea79a6dc9aaded8188e89668de593))
* Add `ruff` to dev dependencies ([22b19bf](https://github.com/Kastakin/PyES/commit/22b19bffcf68f8bc795dbdc769767ccc62cbff64))
* Delete unused script ([4da8353](https://github.com/Kastakin/PyES/commit/4da83531acfb4faa2ec23b7124313faaa876a39f))

## Others
* to 0.4.2 ([78ec1ee](https://github.com/Kastakin/PyES/commit/78ec1ee6fd5b3109abad3001308f86a4cc44cb4d))
* branch 'multi_module' into dev ([dbd5a41](https://github.com/Kastakin/PyES/commit/dbd5a417ae4ae0b99b91b25bbf5029b29e4d42f7))
* Remove unused import ([b6a5bd7](https://github.com/Kastakin/PyES/commit/b6a5bd7ae913f5af3bdf5b87c6493f38c7874c74))
* Relax conv condition for c~=0 ([d5f52ca](https://github.com/Kastakin/PyES/commit/d5f52caf91d8f9b833181293ebd4b6b950fd7828))


# Version v0.4.2

## Features
* Allow change colors in plots ([49610dc](https://github.com/Kastakin/PyES/commit/49610dc3464a39bad4b0c97ebb1318c6ac11d01f))

## Enhancements
* Add example README ([6912940](https://github.com/Kastakin/PyES/commit/6912940055a643cba06fc8208fa24713390ca0e8))
* Preserve indipendent component when switching comp order ([deb32f1](https://github.com/Kastakin/PyES/commit/deb32f146b11644b327148c61a39c649f5080dae))
* Square color pickers in plot window ([16cbfa2](https://github.com/Kastakin/PyES/commit/16cbfa2363ab5bd5b2dfa777ce41afd99bf9aa85))

## Fixes
* Adjust flags behaviour for qt6.4 ([9d5d86a](https://github.com/Kastakin/PyES/commit/9d5d86afb602da3e96eb446d85524605641ec18b))
* Remove unused imports dangling ([b97b7e1](https://github.com/Kastakin/PyES/commit/b97b7e199dfe5e16074c6c47cd37318cfde2658f))
* Avoid recalculating species names in calculation routine ([8f25118](https://github.com/Kastakin/PyES/commit/8f25118545d54615f3057f938f871a29847a7f66))
* Correct error computation of solids ([01db4f2](https://github.com/Kastakin/PyES/commit/01db4f27402dee21fa5df002aae394575059d80e))
* Rename variable for consistency ([31bb88e](https://github.com/Kastakin/PyES/commit/31bb88eea964654bc4137ffa94652aada2062a38))
* Remove unused code ([04d2b54](https://github.com/Kastakin/PyES/commit/04d2b54310b73dd89908d9d23e290ddfd7ca595b))
* Relax damping routine convergence ([26922a5](https://github.com/Kastakin/PyES/commit/26922a56bc99548a3320a54dd2280c796337afe2))

## Chores
* Bump requirements ([3d45733](https://github.com/Kastakin/PyES/commit/3d457336464f3e7bb2d8568976ca536c4de82edc))
* Update release workflow ([784fe30](https://github.com/Kastakin/PyES/commit/784fe30f39dea79a6dc9aaded8188e89668de593))
* Add `ruff` to dev dependencies ([22b19bf](https://github.com/Kastakin/PyES/commit/22b19bffcf68f8bc795dbdc769767ccc62cbff64))
* Delete unused script ([4da8353](https://github.com/Kastakin/PyES/commit/4da83531acfb4faa2ec23b7124313faaa876a39f))

## Others
* branch 'multi_module' into dev ([dbd5a41](https://github.com/Kastakin/PyES/commit/dbd5a417ae4ae0b99b91b25bbf5029b29e4d42f7))
* Remove unused import ([b6a5bd7](https://github.com/Kastakin/PyES/commit/b6a5bd7ae913f5af3bdf5b87c6493f38c7874c74))
* Relax conv condition for c~=0 ([d5f52ca](https://github.com/Kastakin/PyES/commit/d5f52caf91d8f9b833181293ebd4b6b950fd7828))


# Version v0.4.1

## Enhancements
* Adopt different solid computation logic ([](https://github.com/Kastakin/PyES/commit/))

## Fixes
* Export solid distributions in excel/csv ([e1aead0](https://github.com/Kastakin/PyES/commit/e1aead03c50b4de9546380654e51ce0aa4a22213))
* Handle paths with dots in them ([b8d56b6](https://github.com/Kastakin/PyES/commit/b8d56b646cebc964519fa98c42d541dfabc7c1a3))
* Remove print statements ([89a5b1d](https://github.com/Kastakin/PyES/commit/89a5b1d930512209733b2f6fbde3ce4c60529d89))

## Chores
* Run changelog script as tbump hook ([5e09d2e](https://github.com/Kastakin/PyES/commit/5e09d2e51a0f611b46efa446a7770c8eabd23819))
* Create changelog before bumping version ([6c74903](https://github.com/Kastakin/PyES/commit/6c74903142c547b0480f109891af25b53729f769))
* Remove module not used anymore ([ffe0c6e](https://github.com/Kastakin/PyES/commit/ffe0c6ec1fb76bf6dea320042f3e915675b5608a))
* Refactoring and typos ([ada11de](https://github.com/Kastakin/PyES/commit/ada11de3d5ec5b28cc83648babf2058b5bb5bf46))
* Use ubuntu-latest in github runners ([b150c7f](https://github.com/Kastakin/PyES/commit/b150c7fc3ed2b0583fa0a85cc304e0818c48c487))
* Ignore matplotlib to reduce installer size ([d9300d7](https://github.com/Kastakin/PyES/commit/d9300d7256f5fa88efc198d53af388d1b8a7204e))
* Remove unused imports ([65476f4](https://github.com/Kastakin/PyES/commit/65476f43464d93302825a41b06e7bd6980e4fd08))
* Update CHANGELOG ([ae83da0](https://github.com/Kastakin/PyES/commit/ae83da0a3b0481d577834bdca52f3a5b5fc8857c))


# Version v0.4.0

## Features
* Compute solids uncertainty ([7d95e838](https://github.com/Kastakin/PyES/commit/7d95e838d3984ce47d2851e4ded61c9ffedece17))
* Add profiling and benchmarks utilities ([1c150c81](https://github.com/Kastakin/PyES/commit/1c150c812b88617fa98921b05641e8283adee599))
* Allow change colors in plots ([130a92a6](https://github.com/Kastakin/PyES/commit/130a92a66bca0cb7505212d9d9645c95b4d29ea0))

## Enhancements
* Vectorize Jacobian computation ([a72a77e2](https://github.com/Kastakin/PyES/commit/a72a77e2dacfbbfda7f17e6dd75311d39ea49094))
* Minor optimization in speciesConcentrations ([4635b2f1](https://github.com/Kastakin/PyES/commit/4635b2f101f166fcbef24db79a9b2ce85341639d))
* Vectorize error computation operations ([fe215863](https://github.com/Kastakin/PyES/commit/fe215863eaee23ff1679b128afe385a066016e66))
* Testing different damping parameters ([f44770a0](https://github.com/Kastakin/PyES/commit/f44770a012f3d3dc21aa4d9fd548ac15a27f4583))
* Avoid useless nested for loop ([cb413356](https://github.com/Kastakin/PyES/commit/cb41335614ee4276f33995819d00e8fe56e57c0a))
* Allow saving and loading to allow testing ([41fbcada](https://github.com/Kastakin/PyES/commit/41fbcadac323b44bc34dcdadf2f46fc75892cce9))
* Square color pickers in plot window ([ff352c41](https://github.com/Kastakin/PyES/commit/ff352c413f0deea59d0d1914343d5e34d9740b0c))

## Fixes
* Solid sigma is zero if no precipitation ([20b91d54](https://github.com/Kastakin/PyES/commit/20b91d54d5e0b164e114d47465eaafb00890223e))
* Use dummy variable in for loops if possible ([3dc1bc5e](https://github.com/Kastakin/PyES/commit/3dc1bc5e5ea5ae1b90c2d4492a5f154872db757b))
* Avoid useless numpy errors printing ([7d2a2af2](https://github.com/Kastakin/PyES/commit/7d2a2af2aadb31507360852b640d3377782ba467))
* Revert a0 change in damping ([00580970](https://github.com/Kastakin/PyES/commit/00580970dabf471aebf9b351af8cd948ddc558c7))
* Reduce string formatting in logging calls ([97ca1ae0](https://github.com/Kastakin/PyES/commit/97ca1ae0eb2c2b7d126dbc4d0f7c18d5511afcb3))
* Correctly handle checkbox delegate ([66e10e17](https://github.com/Kastakin/PyES/commit/66e10e171240b43d26b5535026c3c97e652f1b4e))
* Correct help_website placeholder link ([a0ac6c2b](https://github.com/Kastakin/PyES/commit/a0ac6c2be460d74b881ecafffe4a55f7df941358))
* Remove unused import ([47f61887](https://github.com/Kastakin/PyES/commit/47f618874e3141242a87239aeb6a97bb4618015e))
* Relax damping routine convergence ([4a45242a](https://github.com/Kastakin/PyES/commit/4a45242a967fd13968465c51eb9458089e7915d3))
* Relax conv condition for c~=0 ([c40c5995](https://github.com/Kastakin/PyES/commit/c40c5995d4b07681d7b47e93911da12999a13dcc))

## Chores
* Fix bump script ([a5bf778a](https://github.com/Kastakin/PyES/commit/a5bf778a352ab7a9924fcdc86a0a2a0eb8a515b0))
* Update build deps ([c3895dff](https://github.com/Kastakin/PyES/commit/c3895dff52f2440d41113ea829d140fc04e55a3f))
* Add pycharm files to .gitignore ([4010d7a2](https://github.com/Kastakin/PyES/commit/4010d7a239c8b5c4ac9bbc674573e8fbd234fb27))
* Poetry update ([c9a7d58a](https://github.com/Kastakin/PyES/commit/c9a7d58a9d240bd2a8acb5323125f69ff2c246e8))
* Script for version bumping/release notes ([03bd378c](https://github.com/Kastakin/PyES/commit/03bd378c012d67704e963a0445833b2201212ad3))
* Update pre-commit hooks ([a749bb27](https://github.com/Kastakin/PyES/commit/a749bb270014e2ec997d5d5a5d4662ac42b072eb))
* Move to stable pyqtrgaph ([c24ab1e4](https://github.com/Kastakin/PyES/commit/c24ab1e412a1449dfabf94e6140881bd607a8463))
* Remove useless readme in icon folder ([2d0c2cc1](https://github.com/Kastakin/PyES/commit/2d0c2cc1440ca0325ffbee92d42f7022ff47269c))
* Add scripts to generate icons ([217c13a6](https://github.com/Kastakin/PyES/commit/217c13a6027c832c882e70d1318140c2a0656908))
* Better naming DBH function ([5694e9f5](https://github.com/Kastakin/PyES/commit/5694e9f5ad306c4b4a04a0f3a3344c41f82815ab))

## Others
* to 0.4.0 ([5c61c684](https://github.com/Kastakin/PyES/commit/5c61c684bce0bf4348cc0bab84ec999480cd8bc1))


