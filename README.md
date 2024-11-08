# 外语教学语料辅助平台

### 介绍
本软件是傲飞平行语料检索（OFA ParaConc）系列软件中的一款，围绕着平行语料双向检索这一核心功能便利外语教师实施外语思政教学与科研活动，同时也适用于英语专业学生的外语学习活动。
本软件编写语言为python 3.8，UTF8编码，采用PySide 6.1.3设计界面，采用PyInstaller进行打包。本版本目前可在windows 7及windows 10窗口环境下运行(64位)。打包文件内含app_data及saved_files两个工作目录，请勿擅自增删相关文件，以免影响软件的正常运行。
本软件内嵌经过精细加工的思政双语语料库一份，因检索所生成的语料仅可用于日常的教、学与科研活动，不可用于任何商业目的。
本软件是辽宁省2023年度职业教育与继续教育教学改革研究项目《思政教学汉英评行语料库的建设与应用》的研究成果之一。本软件的版权归开发者本人所有（软著登字第13473683号）。
![](./app_data/images/flpe_cover.png) 
### 软件功能及使用方法
#### 1. 语料检索功能 
汉英双向检索功能方便用户依据实际需求在汉英两种语言之间进行切换查询。本软件会依据用户输入的语言类型调用不同的检索程序进行英汉正向或反向检索。
##### 1.1 启动软件
进入软件所在文件夹，双击“FLPE.V1.0.exe”可执行文件，等待软件主界面出现。软件启动时会进行内嵌语料库的装载，请耐心等待。
启动后出现初始主界面布局
• 界面最上方为软件图标名称、界面缩小、放大及关闭按钮；
• 其下为菜单栏，包括首页、工具、帮助及关于等；
• 界面主体左侧上半部为加载后的内嵌语料库列表；其下为检索关键词输入框及检索按钮；其下为检索选项区域；其下为检索数据即时统计显示区；其下为进度条；
• 界面左侧顶部为当前语料数据统计及操作选项区域；其下为检索结果显示区域；
• 主界面底端为信息栏。
##### 1.2 设置检索项
在检索选项区域进行检索项设置。
（1）选择检索范围
检索范围共计4种，具体含义如下：
• “全部语料”（默认选项）是指在上方“语料列表”范围内进行检索;
• “所选语料”是指在上方“语料列表”中已选的一个或多个语料中进行检索（注：多选方法为按住Ctrl键点选一个或多个语料名称，或者在点选一个名称后按住Shift键再点选其上或其下任意位置的语料名称）；
• “当前语料”是指通过双击“语料列表”中某一语料名称而激活的单个语料为检索范围；
• “当前体裁”是指以当前语料的体载为参照，检索所有与其同一体裁的语料。
（2）选择检索方式
具体的检索方式分普通检索、拓展检索与正则检索等三种：
• 普通检索：不进行关键词处理，按实际输入检索项进行检索；
• 拓展检索：对英文输入检索项先进行英文词形还原、大小写转换等预处理后再进行检索；
• 正则检索：按实际输入的正则表达式进行检索。
温馨提示：默认选项为拓展检索。当选择正则检索时，软件自动将语料库切换至经过词性赋码后的双语语料库。有关正则表达式的具体含义及用法参见菜单栏上“帮助文档”中的“正则表达式”。
（3）指定展示方式
默认的展示方式是只展示通过输入的检索词检索到的汉英双语句对。如想查看更多相关信息，可指定以下附加展示方式： 
• 展示语源：即附加显示每个双语句对是来源于本语料库中的哪个语料;
• 展示语境：即附加显示每个双语句对所在的段落，亦即段对齐效果；
• 展示注释：即当双语句对中包含注释序号时，附加显示注释序号所指向的内容。
##### 1.3 开始检索 
（1）在检索输入框里输入英文或中文检索词汇，然后点击“检索” 按钮 。报错等提示信息会出现在底端状态栏左侧。
温馨提示：信息提示通常发生于以下几种情况：
• 当输入检索项不符合相应检索模式基本格式时；
• 当检索范围是当前语料，而未指定当前语料时；
• 当检索范围是所选语料，而未进行语料多选时。
（2）点击语料列表各目录，在双击其下任意文件名后，该语料即被指定为“当前语料”，左侧“当前语料区域”将实时显示包括语料标题、日期，及字符数等详细的统计数据。
（3）“检索” 按钮被点击后，软件开始启动线程执行相应的语料检索，左侧底端的进度条会实时显示检索进程，在检索完成后，会刷新进度条上方的语料检索统计数据，并将检索到的句对按指定的方式展示在右侧的检索结果视窗之内。
##### 1.4 查看检索结果
软件界面右侧中下方为检索结果展示窗口。在尚无任何检索结果的情况下，该界面会展示为初始页面。在执行检索后，检索结果将以表格形式展示在检索结果展示窗口内。
详细说明： 
（1）各检索辞条以原文上译文下（亦即中上英下）的方式进行同组分行排列，其前标有分组号、原译文标记。初始状态下各辞条以双语句对齐为基本单位进行展示；检索结果中的检索关键词及双语术语中收录的相应译词分别以红色及蓝色高亮形式突显。
（2）如果选择了附加展示项“展示语境”，检索关键词所在句子将以绿色高亮形式突显。其它展示方式还包括“展示注释”（在原、译文下方展示有可能存在的注释内容）与“展示语源”（该辞条所在语料的具体信息），这些附加信息均以灰色进行展示。
（3）检索结果的页面展示条数为一百组数据；当检索结果组数超过一百条时，检索结果窗口下方的分页展示按钮会亮起。可通过点击该分页按钮查看下一页的具体结果。 
#### 2. 语料阅读功能
语料阅读功能帮助用户对当前语料内容进行单语或双语阅读。
##### 2.1 激活当前语料
双击左侧语料列表中的任意文件，即可将之指定为当前语料。
##### 2.2 选择阅读方式
在界面右上方当前语料选项区内第一个下拉菜单中选取一种阅读模式，即原文段落（默认选项）、译文段落、双语段对齐与双语句对齐，然后再到语料列表中双击任意文章。
##### 2.3 阅读语料内容
当前语料被激活后，软件将依据所指定的阅读模式将语料文本发送到右下的语料内容视窗。
温馨提示：该窗口内的语料文本默认按原文段落排列，这不同于双语段句对齐时原、译文段落有可能被拆分或合并等情况。
##### 2.4 调整字号大小
软件默认字号为12。按Ctrl+上箭头或Ctrl+下箭头，可将当前语料内容展示窗口内文字的字号进行放大到16或缩小至8。
#### 3. 词频统计功能
词频统计功能方便用户获取各类中、英词汇具体使用频率信息。本软件所用语料的具体词性赋码集为PYNLPIR（中文）与PENN（英文），其中的英文部分进行了词形还原处理。相关词性赋码集参见帮助文档中的《词性赋码表》。
##### 3.1 设置选项
CHOOSE  OPTIONS
在主界面点击“统计词频”，弹出词频设置界面，按需设置即可。完成设置后，点击“开始统计”按钮。
温馨提示：
• 缺省设置状态下不进行任何词频过滤处理，对当前语料进行中文词频统计；
• 可按实际需求点选中英文免显选项，选中的类型将不参与词频统计；
• 本软件使用的中英文停用词表文件是位于app/workfiles/目录下的stopword_zh.txt与stopword_en.txt。可在这两份词表中自定义停用词；
• 在自定停用词时不要修改文件名，也不要改变既定格式。
• 若想统计所有语料或选定的若干语料，可先点选“所选语料”或“全部语料”范围，不过参与统计的语料越多，速度自然就会越慢。
##### 3.2 查看词频表
“开始统计”按钮被点击后，词频设置界面会自动关闭，主界面底部状态栏将实时显示词频统计进程;完成词频统计后，会通过弹窗自动展示词频统计结果列表。点击关闭按钮，退出本界面。
温馨提示：
• 此处“首词”即指类符，也就是该词（又称“原形”）及其所有曲折变化词形（又称“家族词”）的统称；
• 词性与词频部分按首词及家庭词的词形、词性以及词频分别显示。
• 有关词性标记的具体说明详见中英文各自的词性赋码集。
• 由于词性赋码采用的是自动标注与人工审校的方式，难免会出现标记不够准确之处。
##### 3.3 输出词频列表
词频列表输出功能方便用户根据实际需求提取出当前生成的词频结果以供后续的NLP处理或研究使用。词频结果可输出为以tab符分隔的TXT文本文件或以表格方式呈现的HTML网页文件。
本软件在词频生成的同时，会将词频列表内容自动保存为本地的txt文本文件及html网页文件，中文文件名为“word_tag_freq_zh_result”，英文文件名为“word_tag_freq_en_result”，可到saved_files目录下查看这些文件。
温馨提示：
为节省空间，每次词频结果文档的输出皆会覆盖之前同名保存的文档；若需要长期使用刚保存的文档，可及时修改当前默认的文件名。
#### 4. 词云绘制功能
词云绘制功能可实现单语或双语词频信息的可视化，使词频分布情况显得更加直观，为外语教学提供便捷的教学素材。
##### 4.1 设置选项
在主界面点击“绘制词云”，弹出词云绘制界面；开始依次设置各参数；完成设置后，点击“开始绘制”按钮。
具体设置方法：
（1）选择词云类型：点选待生成词云类型前的按钮，默认生成类型为“中文词云”；
（2）选择词云范围：点选待生成词云涵盖的语料范围前的按钮，默认为“当前语料”；
（3）设置停用词：点选停用词性和/或停用词表，默认停用词为按词性排除不重要的词汇；
（4）设置其它参数。
温馨提示：
• 请在点击“开始绘制”按钮之前，确保词云范围有效。比如，若选择了“当前语料”，应在此前于语料列表窗口内双击某语料名称激活了当前语料；若选择了“所选语料”，应在此前于语料列表窗口内通过点选多个文件指定了“所选语料”；
• 停用词性默认值参见中英文词性赋码表，可按需增删其内的词性代码；
• 停用词表为本软件使用的第三方库的内嵌词表，该词表位于本软件根目录下；
• 本软件以PNG格式输出图片，背景颜色若为“透明”，则该图片会与其它背景实现自然融合；
• 本软件内嵌有大量蒙板，方便词云拥有灵活多变的图案，这些蒙板位于“app_data/images/cloud_modules/目录下，可在选择蒙板前进入该目录查看各蒙板的序号。
##### 4.2 查看词云
“开始绘制”按钮被点击后，设置界面将自动关闭，词云生成线程将被激活，词云生成进度信息将显示在主界面底端的信息栏内；词云生成后，会自动弹出词云展示窗口。
##### 4.3 保存词云
点击词云展示窗口底端的“保存词云”，当前的词云将以"WORDCLOUD.png"为默认文件名，保存到软件所在根目录下的“saved_files”目录中；当主窗口界面底端信息栏内显示保存成功后，可点击“关闭词云”，退出词云展示窗口。
温馨提示：
为节省空间，每次生成的词云输出时皆会覆盖之前同名保存的词云图片；若需要长期使用刚保存的词云图片，可到该图片所在本地目录中对其当前默认的文件名进行修改。
#### 5. 元素提取功能
元素提取功能可从当前语料中自动提取引言、典故及其他思政元素，为外语教学提供丰富、真实且权威的思政教学素材。
##### 5.1 激活当前语料
如前所述，在主界面双击“语料列表”内的任意文件，即可指定当前语料。
##### 5.2 进入元素提取界面
在主界面点击“提取元素”，即可进入元素提取界面。
温馨提示：“当前语料中文标题”后的文字框若为空白，说明当前语料若未激活，这时若点击“提取引言元素”、“提取其他元素”或“输出结果”，本界面底端的信息栏内均会出现报错提示；在这种情况下，不必关闭本界面，可直接在主窗口界面内通过双击激活当前语料。
##### 5.3 提取引言典故元素
点击“提取引言元素”，本软件将比对内嵌的引言典故知识库，从当前语料库中提取相应的元素；提取成功后，提取结果将直接显示在本界面的“提取结果”视窗内。
温馨提示：
• 元素提取结果将以“元素总数量”-“元素1名称”-“原文”-“译文”-“原典”-“释意”顺序进行展示；
• 元素名称以蓝色突显为辞条名、以红色突显为原文用语。
##### 5.4 提取其他元素
点击“提取其他元素”，本软件将调用月之暗面大语言模型API接口，从当前语料库中联网提取其他元素；在提取过程中，本界面状态栏会显示提取进度及用时，主界面进度条也会实时展示提取进度；提取成功后，提取结果将直接显示在本界面的“提取结果”视窗内。
温馨提示：
• 由于本功能调用了人工智能API接口，在使用时请确保网络畅通；
• 提取时间会略慢些，平均用时约在30秒左右。
##### 5.5 保存提取结果
在元素提取成功后，可点击“输出结果”，将当前窗口展示的提取结果快速保存到本地；点击“关闭退出”，关闭本界面。
温馨提示：提取结果将以“当前语料名称+提取类型”为文件名，并以文本文件形式保存到本软件所在根目录下的"save_files"文件夹中，如“携手推进现代化，共筑命运共同体_其他元素.txt”。
#### 6. 习题抽取功能
习题抽取功能方便使用者从当前语料中随机抽取若干翻译习题，通过练习与比对官方译文提升翻译水平。
##### 6.1 激活当前语料
如前所述，在主界面双击“语料列表”内的任意文件，即可指定当前语料。
##### 6.2 设置选项
在主界面点击“抽取习题”，进入习题抽取界面，按需进行习题抽取设置。
温馨提示：
• 设置翻译方向即指定了试题与参考译文的各自语种，如选择“英译汉”，则抽取的试题为英语，参考译文则为对应的汉语，默认为汉译英；
• 在未勾选“参考译文”的情况下，抽取结果将不包含参考译文，默认为勾选；
• 翻译单位是指试题的形式为一个完整的段落或一个完整的句子，默认为段落；
• 翻译题数最小为1题，最大为10题，默认为5题。
##### 6.3 抽取习题
在完成选项设置后，点击“开始抽取”，抽取成功后，抽取结果将显示在“抽取结果”视窗内。
温馨提示：
• 试题抽取范围涵盖当前语料全部内容，因此标题、作者、日期、小标题，及呼语等单独成段的句子或句子片段将被视为既是段落又是句子的翻译单位进行抽取；
• 试题抽取是随机的，每次抽取都会产生不一样的结果，因此，可反复抽取，直至满意。
##### 6.4 保存习题
试题抽取成功后，可点击“保存结果”，将当前抽取出的试题(及参考译文)保存到本地；点击“关闭退出”，关闭本界面。
温馨提示：提取结果将以“当前语料名称+翻译习题”为文件名，并以文本文件形式保存到本软件所在根目录下的"save_files"文件夹中，如“携手推进现代化，共筑命运共同体_翻译习题.txt”。
#### 7. 语料库自定义功能
语料库自定义功能允许用户对自建的语料库文件进行元素提取，为外语教材思政元素提取与分析创造便利条件。
（1）自建语料库
先参照相关帮助文档提供的方法与流程自建教材语料库，然后再将该语料库所有语料以文件夹的形式放置在本软件根目录下的"app/textbooks/”目录下即可。
（2）进入自定义语料库界面
在主界面点击菜单栏中的“首页”，再点击“教材语料库”，则可进入自定义语料库界面。该界面主要由语料列表、操作按钮、及语料内容展示窗口构成。
（3）查看语料内容
点击左侧语料列表中指定教材名称，显示该教材内部各章节的语料标题，然后再双击任意章节，即可将该语料的文本载入右侧“课文内容”展示窗口之内。
（4）提取元素
在成功载入某个语料内容之后，点击左下方“提取元素”按钮，进行元素提取，提取进程及信息将实时显示在其下的进度条及状态栏内；元素若提取成功，则展示窗口将从“课文内容”自动跳转到“AI提取结果”展示窗口。
温馨提示：
• 本功能调用了人工智能API接口，在使用时请确保网络畅通；
• 提取时间因当前语料大小而略有不同，平均用时约在15秒左右。
（5）保存提取结果
在元素提取成功后，可点击“保存结果”，将当前窗口展示的提取结果快速保存到本地，下方状态栏会显示文件保存是否成功；点击“关闭退出”，关闭本界面。
温馨提示：提取结果将以“当前语料名称+提取类型”为文件名，并以文本文件形式保存到本软件所在根目录下的"save_files"文件夹中，如“SEMH_B1C12U30_elm.txt”。elm即element的缩写。
#### 8. 其他功能
##### 8.1 字号调节
本软件具有字号调节功能，可通过点击“工具/字号调节”或使用相应的快捷键对文本视窗内的文本字号进行适度放大或缩小。
• 方法一：在文本视窗被激活后，点击主界面上方菜单栏上的“工具”，再点击“字号调整”，再点击“+”或“-”号；
• 方法二：在文本视窗被激活后，按“Ctrl+上箭头”或按“Ctrl+下箭头”，对文本视窗内的文本字号进行放大或缩小调整。
温馨提示：
• 文本视窗的缺省字号值为12，可调节最小值为8，最大值为16;
• 方法一仅适用于主界面的检索结果视窗内的文本。
##### 8.2 语料维护
语料维护功能提供停用词表更新、双语术语词表更新，及引言典故知识库的更新服务。
8.2.1 更新停用词表
停用词表在词频生成、词云绘制等方面能够发挥重要作用。点击“更新中文（或英文）停用词表”，在弹出的停用词表视窗中直接增加、修改或删除指定辞条，然后点击“保存语料”，“关闭退出”即可。
8.2.2 更新双语术语词表
双语术语词表可保证双语检索结果能够实现检索关键词的双语突显，为检索结果的阅读提供方便。
点击“更新引言词库”，在弹出的双语术语词表视窗中的任意位置，先增加换行符，然后再加入新辞条，即可实现辞条的增加；也可以修改或删除任意辞条，然后点击“保存语料”，“关闭退出”即可。
温馨提示：在增、删，或修改双语辞条时，要注意保持术语格式正确，即：
• 原语与译语之间用一个TAB键分隔；
• 原语列不能出现重复项；
• 译语列用“|”将一词的多个译文连接在一起
8.2.3 更新引言典故知识库
引言典故知识库是引言典故元素提取功能得以实现的根本保障。
（1）进入知识库界面
点击“更新引言词库”，即可弹出引言语料编辑界面；
（2）辞条查看及载入
点击“引言”右侧的下拉菜单按钮，能看到所有的引言辞条，点击任一辞条，即可载入该辞条的全部内容。
（3）删除辞条
点击“删除辞条”，然后再点击“保存语料”，即可完成对当前辞条的删除；随后点击“关闭退出”即可。
温馨提示：删除后的辞条不可恢复，因此在进行辞条删除操作时要谨慎。
（4）修改辞条
先对当前辞条各文本输入框内的文字进行修改，然后点击“修改辞条”，再点击“保存语料”，即可完成对当前辞条的修改；随后点击“关闭退出”即可。
温馨提示：
• 当前辞条的序号项及引言项不可修改；
• “变体”是指辞条有可能以其他形式出现在文本当中，变体可以是一个，也可以是多个，多个变体之间用“|”号连接。
• 在进行引言典故抽取时，系统将以辞条名称及其各变体名称展开细致而全面的检索。
（5）新增辞条
先在当前辞条下方的“新增”文本输入框内输入新辞条名称，再点击“新增辞条”按钮，界面会转换成新增辞条编辑界面；然后通过查询资料，补入相关知识，然后点击“修改辞条”，最后再点击“保存语料”，即完成了词条的新增；最后点击“关闭退出”即可。
温馨提示：
当新增辞名称与辞条目录中的名称重复时，界面底端的状态栏会显示创建失败信息。
##### 8.3 检索结果输出
点击主界面顶部菜单栏中的“工具”，在其下拉菜单中点击语料输出，再点击检索结果存贮文件格式，当前检索结果将以指定的文件格式保存到本地。
温馨提示：
• 在输出检索结果之前要确保已完成了语料检索，否则会提示检索结果不存在；
• 检索结果保存在本软件所在根目录下的“saved_files”之中，默认名称为“current_concordance_result.txt”；每次输出都会覆盖该文档，因此若需要长期保存该文档，请及时更改文件名。
• 以html格式保存当前检索结果将获得与检索窗口同样的展示效果；
• 以txt格式保存的文件，将用tab键表达单元格之间的分隔线，将以符号“【】”表达高亮显示的关键词，同时会将表格中合并显示的序列号分开显示在原文与译文之前。
• 以txt格式保存的文本内容可直接复制到excel表格中，生成表格形式的数据。
##### 8.4 语料库自动更新
由于本软件内嵌语料库制作过程较为复杂，新增数据将由软件开发者定期完成。
（1）获取更新数据
需要更新时，可通过软件上的联系方式联系作者，询问更新情况，索取json格式的新数据；
（2）自动更新语料库
将接收到的json数据文件放入本软件根目下的“app_data/corpus/”目录下，然后再启动本软件，软件会在载入内嵌语料库时会自动识别、转码新增数据，进而以dat格式将之保存到“app_data/temp_data/”目录下，最终完成语料库更新。
温馨提示：
• 由于转码时需要进行大量数据提取、统计与运算等操作，因此转码过程有可能会较慢，需要耐心等待1到数分钟；
若希望自己能够随时更新数据，可联系作者，获取语料库制作规范、流程及工具等资料，然后再依据这些资料进行双语语料的采集、清洁、对齐、双语赋码、打包成json等操作。
##### 8.5 输入提示
输入提示方便用户高效点选检索关键词。 
使用方法：在输入框里输入英文或中文检索词汇时，输入框会出现悬浮条来展示一个或多个以相应词汇开头的检索词汇，以供用户参考。
温馨提示：这些推荐检索词均来自于位于本软件安装目录/app_data/workfiles目录下的双语术语文件bi_term_dict.txt。用户可根据自身的实际需要，随时修改该文件里的具体辞条，但修改时要注意保持相应的格式（一行一辞条；每行中文在前，英文在后或无英文，两者之间用tab分隔；多个英文术语之间用|号进行分隔），不要对该文件名进行任何修改。
##### 8.6 操作提示
操作提示功能方便用户了解界面各组件基本功能及把握检索进程的具体状况。提示信息以悬浮文字及底部状态栏文字等两种方式进行展示。
温馨提示：
• 将鼠标置于某组件之上并停留片刻，即可看到相应组件的基本功能提示信息；
• 在进行具体检索操作时，在底部状态栏左侧位置可看到输入是否合法、检索结果具体组数与条数、操作进度提示等各类提示信息。
##### 8.7 文档帮助
点击主界面顶部菜单栏中的“帮助”，在其下拉菜单中可点击查看与本软件使用相关的帮助文档。 
#### 搭建运行环境
##### 1. 第三方库列表
PySide6==6.1.3
PySide6-Addons==6.3.1
PySide6-Essentials==6.3.1
pydantic==2.6.0
pandas==1.5.3
Pillow==9.0.1
wordcloud==1.8.2.2
imageio==2.26.0
openai==1.7.0
python-dotenv==0.20.0
pywin32-ctypes==0.2.3
pyinstaller==6.10.0  
##### 2. 打包软件安装与程序打包
pip install pyinstaller
pyinstaller -F -w main.py
