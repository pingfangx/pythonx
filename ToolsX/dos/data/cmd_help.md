

# 【1/86】ASSOC
```
显示或修改文件扩展名关联

ASSOC [.ext[=[fileType]]]

  .ext      指定跟文件类型关联的文件扩展名
  fileType  指定跟文件扩展名关联的文件类型

键入 ASSOC 而不带参数，显示当前文件关联。如果只用文件扩展
名调用 ASSOC，则显示那个文件扩展名的当前文件关联。如果不为
文件类型指定任何参数，命令会删除文件扩展名的关联。

```

# 【2/86】ATTRIB
```
显示或更改文件属性。

ATTRIB [+R | -R] [+A | -A ] [+S | -S] [+H | -H] [+I | -I]
       [drive:][path][filename] [/S [/D] [/L]]
  + 设置属性。
  - 清除属性。
  R 只读文件属性。
  A 存档文件属性。
  S 系统文件属性。
  H 隐藏文件属性。
  I 无内容索引文件属性。
  [drive:][path][filename]
      指定 attrib 要处理的文件。
  /S 处理当前文件夹及其所有子文件夹中的匹配文件。
  /D 也处理文件夹。
  /L 处理符号链接和符号链接目标的属性。


```

# 【3/86】BREAK
```
设置或清除 DOS 系统的扩展 CTRL+C 检测

这个命令是为了与 DOS 系统的兼容而保留的，在 Windows 
里不起作用。

如果命令扩展被启用，并且操作平台是 Windows，
BREAK 命令会在被调试程序调试时输入一个硬代码中断点。

```

# 【4/86】BCDEDIT
```

BCDEDIT - 启动配置数据存储编辑器

Bcdedit.exe 命令行工具用于修改启动配置数据存储。
启动配置数据存储包含启动配置参数并控制操作系统的启动方式。这些参数以前位于
Boot.ini 文件中(在基于 BIOS 的操作系统中)或位于稳定 RAM 项中(在基于可扩展
固件接口的操作系统中)。可以使用 Bcdedit.exe 在启动配置数据存储中添加、删除、
编辑和附加项。

有关命令和选项的详细信息，请键入 bcdedit.exe /? <command>。
例如，若要显示有关 /createstore 命令的详细信息，请键入:

     bcdedit.exe /? /createstore

有关本帮助文件中按字母顺序排列的主题列表，请运行 "bcdedit /? TOPICS"。

对存储执行的命令
================================
/createstore    新建空的启动配置数据存储。
/export         将系统存储的内容导出到文件。以后可以使用该文件还原系统
                存储的状态。
/import         使用 /export 命令创建的备份文件来还原系统存储的状态。                
/sysstore       设置系统存储设备(仅影响 EFI 系统，在重新启动后不再有效，
                且仅用于系统存储设备不确定的情况下)。

对存储中的项执行的命令
===========================================
/copy           复制存储中的项。
/create         在存储中新建项。
/delete         删除存储中的项。
/mirror         创建存储中项的镜像。

运行 bcdedit /? ID 可获得有关这些命令使用的标识符的信息。

对项选项执行的命令
======================================
/deletevalue    删除存储中的项选项。
/set            设置存储中的项选项值。

运行 bcdedit /? TYPES 可获得这些命令使用的数据类型的列表。
运行 bcdedit /? FORMATS 可获得有效数据格式的列表。

控制输出的命令
============================
/enum           列出存储中的项。
/v              命令行选项，完整显示项标识符，而不是使用已知标识符的名称。                
                单独使用命令 /v 可完整显示活动类型的项标识符。                

单独运行 "bcdedit" 等同于运行 "bcdedit /enum ACTIVE"。

控制启动管理器的命令
======================================
/bootsequence   为启动管理器设置一次性启动序列。
/default        设置启动管理器将使用的默认项。
/displayorder   设置启动管理器显示多重引导菜单的顺序。                
/timeout        设置启动管理器的超时值。
/toolsdisplayorder  设置启动管理器显示工具菜单的顺序。                    

控制启动应用程序紧急管理服务的命令
==========================================================================
/bootems        启用或禁用启动应用程序的紧急管理服务。                
/ems            启用或禁用操作系统项的紧急管理服务。                
/emssettings    设置全局紧急管理服务参数。

控制调试的命令
==============================
/bootdebug      启用或禁用启动应用程序的启动调试。
/dbgsettings    设置全局调试程序参数。
/debug          启用或禁用操作系统项的内核调试。                
/hypervisorsettings  设置虚拟机监控程序的参数。


```

# 【5/86】CACLS
```


 注意: 不推荐使用 Cacls，请使用 Icacls。



 显示或者修改文件的访问控制列表(ACL)



 CACLS filename [/T] [/M] [/L] [/S[:SDDL]] [/E] [/C] [/G user:perm]

        [/R user [...]] [/P user:perm [...]] [/D user [...]]

    filename      显示 ACL。

    /T            更改当前目录及其所有子目录中

                  指定文件的 ACL。

    /L            对照目标处理符号链接本身

    /M            更改装载到目录的卷的 ACL

    /S            显示 DACL 的 SDDL 字符串。

    /S:SDDL       使用在 SDDL 字符串中指定的 ACL 替换 ACL。

                  (/E、/G、/R、/P 或 /D 无效)。

    /E            编辑 ACL 而不替换。

    /C            在出现拒绝访问错误时继续。

    /G user:perm  赋予指定用户访问权限。

                  Perm 可以是: R  读取

                               W  写入

                               C  更改(写入)

                               F  完全控制

    /R user       撤销指定用户的访问权限(仅在与 /E 一起使用时合法)。

    /P user:perm  替换指定用户的访问权限。

                  Perm 可以是: N  无

                               R  读取

                               W  写入

                               C  更改(写入)

                               F  完全控制

    /D user       拒绝指定用户的访问。

 在命令中可以使用通配符指定多个文件。

 也可以在命令中指定多个用户。



缩写:

    CI - 容器继承。

         ACE 会由目录继承。

    OI - 对象继承。

         ACE 会由文件继承。

    IO - 只继承。

         ACE 不适用于当前文件/目录。

    ID - 已继承。

         ACE 从父目录的 ACL 继承。


```

# 【6/86】CALL
```
从批处理程序调用另一个批处理程序。

CALL [drive:][path]filename [batch-parameters]

  batch-parameters   指定批处理程序所需的命令行信息。

如果命令扩展被启用，CALL 会如下改变:

CALL 命令现在将卷标当作 CALL 的目标接受。语法是:

    CALL:label arguments

一个新的批文件上下文由指定的参数所创建，控制在卷标被指定
后传递到语句。您必须通过达到批脚本文件末两次来 "exit" 两次。
第一次读到文件末时，控制会回到 CALL 语句的紧后面。第二次
会退出批脚本。键入 GOTO /?，参看 GOTO :EOF 扩展的描述，
此描述允许您从一个批脚本返回。

另外，批脚本文本参数参照(%0、%1、等等)已如下改变:


     批脚本里的 %* 指出所有的参数(如 %1 %2 %3 %4 %5 ...)

     批参数(%n)的替代已被增强。您可以使用以下语法:

         %~1         - 删除引号(")，扩展 %1
         %~f1        - 将 %1 扩展到一个完全合格的路径名
         %~d1        - 仅将 %1 扩展到一个驱动器号
         %~p1        - 仅将 %1 扩展到一个路径
         %~n1        - 仅将 %1 扩展到一个文件名
         %~x1        - 仅将 %1 扩展到一个文件扩展名
         %~s1        - 扩展的路径只含有短名
         %~a1        - 将 %1 扩展到文件属性
         %~t1        - 将 %1 扩展到文件的日期/时间
         %~z1        - 将 %1 扩展到文件的大小
         %~$PATH:1   - 查找列在 PATH 环境变量的目录，并将 %1
                       扩展到找到的第一个完全合格的名称。如果
                       环境变量名未被定义，或者没有找到文件，
                       此修改符会扩展到空字符串

    可以组合修改符来取得多重结果:

        %~dp1       - 只将 %1 扩展到驱动器号和路径
        %~nx1       - 只将 %1 扩展到文件名和扩展名
        %~dp$PATH:1 - 在列在 PATH 环境变量中的目录里查找 %1，
                      并扩展到找到的第一个文件的驱动器号和路径。
        %~ftza1     - 将 %1 扩展到类似 DIR 的输出行。

    在上面的例子中，%1 和 PATH 可以被其他有效数值替换。
    %~ 语法被一个有效参数号码终止。%~ 修定符不能跟 %*
    使用

```

# 【7/86】CD
```
显示当前目录名或改变当前目录。

CHDIR [/D] [drive:][path]
CHDIR [..]
CD [/D] [drive:][path]
CD [..]

  ..   指定要改成父目录。

键入 CD drive: 显示指定驱动器中的当前目录。
不带参数只键入 CD，则显示当前驱动器和目录。

使用 /D 开关，除了改变驱动器的当前目录之外，
还可改变当前驱动器。

如果命令扩展被启用，CHDIR 会如下改变:

当前的目录字符串会被转换成使用磁盘名上的大小写。所以，
如果磁盘上的大小写如此，CD C:\TEMP 会将当前目录设为
C:\Temp。

CHDIR 命令不把空格当作分隔符，因此有可能将目录名改为一个
带有空格但不带有引号的子目录名。例如:

     cd \winnt\profiles\username\programs\start menu

与下列相同:  

     cd "\winnt\profiles\username\programs\start menu" 

在扩展停用的情况下，您必须键入以上命令。

```

# 【8/86】CHCP
```
显示或设置活动代码页编号。

CHCP [nnn]

  nnn   指定代码页编号。

不带参数键入 CHCP 以显示活动代码页编号。

```

# 【9/86】CHDIR
```
显示当前目录名或改变当前目录。

CHDIR [/D] [drive:][path]
CHDIR [..]
CD [/D] [drive:][path]
CD [..]

  ..   指定要改成父目录。

键入 CD drive: 显示指定驱动器中的当前目录。
不带参数只键入 CD，则显示当前驱动器和目录。

使用 /D 开关，除了改变驱动器的当前目录之外，
还可改变当前驱动器。

如果命令扩展被启用，CHDIR 会如下改变:

当前的目录字符串会被转换成使用磁盘名上的大小写。所以，
如果磁盘上的大小写如此，CD C:\TEMP 会将当前目录设为
C:\Temp。

CHDIR 命令不把空格当作分隔符，因此有可能将目录名改为一个
带有空格但不带有引号的子目录名。例如:

     cd \winnt\profiles\username\programs\start menu

与下列相同:  

     cd "\winnt\profiles\username\programs\start menu" 

在扩展停用的情况下，您必须键入以上命令。

```

# 【10/86】CHKDSK
```
检查磁盘并显示状态报告。


CHKDSK [volume[[path]filename]]] [/F] [/V] [/R] [/X] [/I] [/C] [/L[:size]] [/B]


  volume         指定驱动器号(后面跟一个冒号)、
装入点或卷名。
  filename        仅用于 FAT/FAT32: 指定要检查是否有碎片的文件。
  /F              修复磁盘上的错误。
  /V              在 FAT/FAT32 上: 显示磁盘上每个文件的
完整路径和名称。
                  在 NTFS 上: 如果有清除消息，则显示。
  /R              查找损坏的扇区并恢复可读信息
                  (隐含 /F)。
  /L:size         仅用于 NTFS:  将日志文件大小更改为指定的 KB 数。如果未
                  指定大小，则显示当前
                  大小。
  /X              如果必要，则先强制卸除卷。
                  该卷的所有打开句柄都会无效
                  (隐含 /F)。
  /I              仅用于 NTFS: 对索引项进行强度较小的检查。
  /C              仅用于 NTFS: 跳过文件夹结构的
                  循环检查。
  /B              仅用于 NTFS: 重新评估该卷上的坏簇
                  (隐含 /R)

/I 或 /C 开关通过跳过对该卷的某些检查，
可减少运行 Chkdsk 所需的时间。

```

# 【11/86】CHKNTFS
```
启动时显示或修改磁盘检查。

CHKNTFS volume [...]
CHKNTFS /D
CHKNTFS /T[:time]
CHKNTFS /X volume [...]
CHKNTFS /C volume [...]

  volume         指定驱动器号(后面跟一个冒号)、装入点或卷名。
  /D             将计算机还原为默认行为；
                 启动时检查所有驱动器，并对有问题的驱动器运行 chkdsk。
  /T:time        将 AUTOCHK 初始递减计数时间
                 更改为指定的时间，单位为秒。
                 如果没有指定时间，则显示当前设置。
  /X             将驱动器排除在启动时检查范围之外。被排除的驱动器在命令调用之间不会
                 累计。
  /C             安排驱动器在启动时检查；
                 如果驱动器有问题，则运行 chkdsk。

如果未指定开关，CHKNTFS 将显示指定的驱动器是否有问题
或者是否计划在下一次重新启动时执行检查。

```

# 【12/86】CLS
```
清除屏幕。

CLS

```

# 【13/86】CMD
```
启动 Windows 命令解释器的一个新实例

CMD [/A | /U] [/Q] [/D] [/E:ON | /E:OFF] [/F:ON | /F:OFF] [/V:ON | /V:OFF]
    [[/S] [/C | /K] string]

/C      执行字符串指定的命令然后终止
/K      执行字符串指定的命令但保留
/S      修改 /C 或 /K 之后的字符串处理(见下)
/Q      关闭回显
/D      禁止从注册表执行 AutoRun 命令(见下)
/A      使向管道或文件的内部命令输出成为 ANSI
/U      使向管道或文件的内部命令输出成为
        Unicode
/T:fg   设置前台/背景颜色(详细信息见 COLOR /?)
/E:ON   启用命令扩展(见下)
/E:OFF  禁用命令扩展(见下)
/F:ON   启用文件和目录名完成字符(见下)
/F:OFF  禁用文件和目录名完成字符(见下)
/V:ON   使用 ! 作为分隔符启用延迟的环境变量
        扩展。例如，/V:ON 会允许 !var! 在执行时
        扩展变量 var。var 语法会在输入时
        扩展变量，这与在一个 FOR
        循环内不同。
/V:OFF  禁用延迟的环境扩展。

注意，如果字符串加有引号，可以接受用命令分隔符 "&&"
分隔多个命令。另外，由于兼容性
原因，/X 与 /E:ON 相同，/Y 与 /E:OFF 相同，且 /R 与
/C 相同。任何其他开关都将被忽略。

如果指定了 /C 或 /K，则会将该开关之后的
命令行的剩余部分作为一个命令行处理，其中，会使用下列逻辑
处理引号(")字符:

    1.  如果符合下列所有条件，则会保留
        命令行上的引号字符:

        - 不带 /S 开关
        - 正好两个引号字符
        - 在两个引号字符之间无任何特殊字符，
          特殊字符指下列字符: &<>()@^|
        - 在两个引号字符之间至少有
          一个空格字符
        - 在两个引号字符之间的字符串是某个
          可执行文件的名称。

    2.  否则，老办法是看第一个字符
        是否是引号字符，如果是，则去掉首字符并
        删除命令行上最后一个引号，保留
        最后一个引号之后的所有文本。

如果 /D 未在命令行上被指定，当 CMD.EXE 开始时，它会寻找
以下 REG_SZ/REG_EXPAND_SZ 注册表变量。如果其中一个或
两个都存在，这两个变量会先被执行。

    HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\AutoRun

        和/或

    HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun

命令扩展是按默认值启用的。您也可以使用 /E:OFF ，为某一
特定调用而停用扩展。您
可以在机器上和/或用户登录会话上
启用或停用 CMD.EXE 所有调用的扩展，这要通过设置使用
REGEDIT.EXE 的注册表中的一个或两个 REG_DWORD 值:

    HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\EnableExtensions

        和/或

    HKEY_CURRENT_USER\Software\Microsoft\Command Processor\EnableExtensions

到 0x1 或 0x0。用户特定设置
比机器设置有优先权。命令行
开关比注册表设置有优先权。

在批处理文件中，SETLOCAL ENABLEEXTENSIONS 或 DISABLEEXTENSIONS 参数
比 /E:ON 或 /E:OFF 开关有优先权。请参阅 SETLOCAL /? 获取详细信息。

命令扩展包括对下列命令所做的
更改和/或添加:

    DEL or ERASE
    COLOR
    CD or CHDIR
    MD or MKDIR
    PROMPT
    PUSHD
    POPD
    SET
    SETLOCAL
    ENDLOCAL
    IF
    FOR
    CALL
    SHIFT
    GOTO
    START (同时包括对外部命令调用所做的更改)
    ASSOC
    FTYPE

有关特定详细信息，请键入 commandname /? 查看。

延迟环境变量扩展不按默认值启用。您
可以用/V:ON 或 /V:OFF 开关，为 CMD.EXE 的某个调用而
启用或停用延迟环境变量扩展。您
可以在机器上和/或用户登录会话上启用或停用 CMD.EXE 所有
调用的延迟扩展，这要通过设置使用 REGEDIT.EXE 的注册表中的
一个或两个 REG_DWORD 值:

    HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\DelayedExpansion

        和/或

    HKEY_CURRENT_USER\Software\Microsoft\Command Processor\DelayedExpansion

到 0x1 或 0x0。用户特定设置
比机器设置有优先权。命令行开关
比注册表设置有优先权。

在批处理文件中，SETLOCAL ENABLEDELAYEDEXPANSION 或 DISABLEDELAYEDEXPANSION
参数比 /V:ON 或 /V:OFF 开关有优先权。请参阅 SETLOCAL /? 
获取详细信息。

如果延迟环境变量扩展被启用，
惊叹号字符可在执行时间被用来
代替一个环境变量的数值。

您可以用 /F:ON 或 /F:OFF 开关为 CMD.EXE 的某个
调用而启用或禁用文件名完成。您可以在计算上和/或
用户登录会话上启用或禁用 CMD.EXE 所有调用的完成，
这可以通过使用 REGEDIT.EXE 设置注册表中的下列
 REG_DWORD 的全部或其中之一:

    HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\CompletionChar
    HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\PathCompletionChar

        和/或

    HKEY_CURRENT_USER\Software\Microsoft\Command Processor\CompletionChar
    HKEY_CURRENT_USER\Software\Microsoft\Command Processor\PathCompletionChar

由一个控制字符的十六进制值作为一个特定参数(例如，0x4
是Ctrl-D，0x6 是 Ctrl-F)。用户特定设置优先于机器设置。
命令行开关优先于注册表设置。

如果完成是用 /F:ON 开关启用的，两个要使用的控制符是: 
目录名完成用 Ctrl-D，文件名完成用 Ctrl-F。要停用
注册表中的某个字符，请用空格(0x20)的数值，因为此字符
不是控制字符。

如果键入两个控制字符中的一个，完成会被调用。完成功能将
路径字符串带到光标的左边，如果没有通配符，将通配符附加
到左边，并建立相符的路径列表。然后，显示第一个相符的路
径。如果没有相符的路径，则发出嘟嘟声，不影响显示。之后，
重复按同一个控制字符会循环显示相符路径的列表。将 Shift 
键跟控制字符同时按下，会倒着显示列表。如果对该行进行了
任何编辑，并再次按下控制字符，保存的相符路径的列表会被
丢弃，新的会被生成。如果在文件和目录名完成之间切换，会
发生同样现象。两个控制字符之间的唯一区别是文件完成字符
符合文件和目录名，而目录完成字符只符合目录名。如果文件
完成被用于内置式目录命令(CD、MD 或 RD)，就会使用目录
完成。
用引号将相符路径括起来，完成代码可以正确处理含有空格
或其他特殊字符的文件名。同时，如果备份，然后从行内调用
文件完成，完成被调用时位于光标右方的文字会被调用。

需要引号的特殊字符是:
     <space>
     ()[]{}^=;!'+,`~(&()

```

# 【14/86】COLOR
```
设置默认的控制台前景和背景颜色。

COLOR [attr]

  attr        指定控制台输出的颜色属性

颜色属性由两个十六进制数字指定 -- 第一个为背景，第二个则为
前景。每个数字可以为以下任何值之一:

    0 = 黑色       8 = 灰色
    1 = 蓝色       9 = 淡蓝色
    2 = 绿色       A = 淡绿色
    3 = 浅绿色     B = 淡浅绿色
    4 = 红色       C = 淡红色
    5 = 紫色       D = 淡紫色
    6 = 黄色       E = 淡黄色
    7 = 白色       F = 亮白色

如果没有给定任何参数，该命令会将颜色还原到 CMD.EXE 启动时
的颜色。这个值来自当前控制台窗口、/T 命令行开关或 
DefaultColor 注册表值。

如果用相同的前景和背景颜色来执行 COLOR 命令，COLOR 命令
会将 ERRORLEVEL 设置为 1。

例如: "COLOR fc" 在亮白色上产生亮红色

```

# 【15/86】COMP
```
比较两个文件或两个文件集的内容。

COMP [data1] [data2] [/D] [/A] [/L] [/N=number] [/C] [/OFF[LINE]]

  data1      指定要比较的第一个文件的位置和名称。
  data2      指定要比较的第二个文件的位置和名称。
  /D         以十进制格式显示差异。
  /A         以 ASCII 字符显示差异。
  /L         显示不同的行数。
  /N=number  只比较每个文件中第一个指定的行数。
  /C         比较文件时 ASCII 字母不区分大小写。
  /OFF[LINE] 不要跳过带有脱机属性集的文件。

要比较文件集，请在 data1 和 data2 参数中使用通配符。

```

# 【16/86】COMPACT
```
显示或改变 NTFS 分区上文件的压缩.

COMPACT [/C | /U] [/S[:dir]] [/A] [/I] [/F] [/Q] [filename [...]]

  /C        压缩指定的文件。会给目录作标记，这样以后添加的文件
            会得到压缩。
  /U        解压缩指定的文件。会给目录作标记，这样以后添加的文
            件不会得到压缩。
  /S        在指定的目录和所有子目录中的文件上执行指定操作。
            默认 "dir"是当前目录。
  /A        显示具有隐藏或系统属性的文件。在默认
            情况下，这些文件都是被忽略的。
  /I        即使在错误发生后，依然继续执行指定的操作。在默认情况
            下，COMPACT 在遇到错误时会停止。
  /F        在所有指定文件上强制压缩操作，包括已被压缩的文件。
            在默认情况下，已经压缩的文件被忽略。
  /Q        只报告最重要的信息。
  filename  指定类型、文件和目录。

  不跟参数一起使用时，COMPACT 显示当前目录及其所含文件的
  压缩状态。您可以使用多个文件名和通配符。在多个参数之间
  必须加空格。

```

# 【17/86】CONVERT
```
将 FAT 卷转换为 NTFS。

CONVERT volume /FS:NTFS [/V] [/CvtArea:filename] [/NoSecurity] [/X]


  volume      指定驱动器号(后面跟一个冒号)、装入点或卷名。
  /FS:NTFS    指定要将此卷转换为 NTFS。
  /V          指定将在详细模式下运行 Convert。
  /CvtArea:filename
              指定根目录中的一个连续文件，该文件
              将是 NTFS 系统文件的占位符。
  /NoSecurity 指定所有用户均可以访问
              转换文件和目录的安全设置。
  /X          如果必要，请先强制卸除卷。
              该卷的所有打开句柄将会无效。

```

# 【18/86】COPY
```
将一份或多份文件复制到另一个位置。

COPY [/D] [/V] [/N] [/Y | /-Y] [/Z] [/L] [/A | /B ] source [/A | /B]
     [+ source [/A | /B] [+ ...]] [destination [/A | /B]]

  source       指定要复制的文件。
  /A           表示一个 ASCII 文本文件。
  /B           表示一个二进位文件。
  /D           允许解密要创建的目标文件
  destination  为新文件指定目录和/或文件名。
  /V           验证新文件写入是否正确。
  /N           复制带有非 8dot3 名称的文件时，
               尽可能使用短文件名。
  /Y           不使用确认是否要覆盖现有目标文件
               的提示。
  /-Y          使用确认是否要覆盖现有目标文件
               的提示。
  /Z           用可重新启动模式复制已联网的文件。
/L           如果源是符号链接，请将链接复制
               到目标而不是源链接指向的实际文件。

命令行开关 /Y 可以在 COPYCMD 环境变量中预先设定。
这可能会被命令行上的 /-Y 替代。除非 COPY
命令是在一个批处理脚本中执行的，默认值应为
在覆盖时进行提示。

要附加文件，请为目标指定一个文件，为源指定
数个文件(用通配符或 file1+file2+file3 格式)。

```

# 【19/86】DATE
```
显示或设置日期。

DATE [/T | date]

显示当前日期设置和输入新日期的提示，请键入
不带参数的 DATE。要保留现有日期，请按 Enter。

如果命令扩展被启用，DATE 命令会支持 /T 开关；
该开关指示命令只输出当前日期，但不提示输入新日期。

```

# 【20/86】DEL
```
删除一个或数个文件。

DEL [/P] [/F] [/S] [/Q] [/A[[:]attributes]] names
ERASE [/P] [/F] [/S] [/Q] [/A[[:]attributes]] names

  names         指定一个或多个文件或者目录列表。
                通配符可用来删除多个文件。
                如果指定了一个目录，该目录中的所
                有文件都会被删除。

  /P            删除每一个文件之前提示确认。
  /F            强制删除只读文件。
  /S            删除所有子目录中的指定的文件。
  /Q            安静模式。删除全局通配符时，不要求确认
  /A            根据属性选择要删除的文件
  属性          R  只读文件                     S  系统文件
                H  隐藏文件                     A  存档文件
                I  无内容索引文件               L  重分析点
                -  表示“否”的前缀

如果命令扩展被启用，DEL 和 ERASE 更改如下:

/S 开关的显示句法会颠倒，即只显示已经
删除的文件，而不显示找不到的文件。

```

# 【21/86】DIR
```
显示目录中的文件和子目录列表。

DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
  [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]

  [drive:][path][filename]
              指定要列出的驱动器、目录和/或文件。

  /A          显示具有指定属性的文件。
  属性         D  目录                R  只读文件
               H  隐藏文件            A  准备存档的文件
               S  系统文件            I  无内容索引文件
               L  解析点             -  表示“否”的前缀
  /B          使用空格式(没有标题信息或摘要)。
  /C          在文件大小中显示千位数分隔符。这是默认值。用 /-C 来
              禁用分隔符显示。
  /D          跟宽式相同，但文件是按栏分类列出的。
  /L          用小写。
  /N          新的长列表格式，其中文件名在最右边。
  /O          用分类顺序列出文件。
  排列顺序     N  按名称(字母顺序)     S  按大小(从小到大)
               E  按扩展名(字母顺序)   D  按日期/时间(从先到后)
               G  组目录优先           -  反转顺序的前缀
  /P          在每个信息屏幕后暂停。
  /Q          显示文件所有者。
  /R          显示文件的备用数据流。
  /S          显示指定目录和所有子目录中的文件。
  /T          控制显示或用来分类的时间字符域。
  时间段      C  创建时间
              A  上次访问时间
              W  上次写入的时间
  /W          用宽列表格式。
  /X          显示为非 8.3 文件名产生的短名称。格式是 /N 的格式，
              短名称插在长名称前面。如果没有短名称，在其位置则
              显示空白。
  /4          用四位数字显示年

可以在 DIRCMD 环境变量中预先设定开关。通过添加前缀 - (破折号)
来替代预先设定的开关。例如，/-W。

```

# 【22/86】DISKCOMP
```
比较两张软盘的内容。

DISKCOMP [drive1: [drive2:]]


```

# 【23/86】DISKCOPY
```
把一张软盘的内容复制到另一张。

DISKCOPY [drive1: [drive2:]] [/V]

  /V   验证信息是否已正确复制。

两张软盘的类型必须相同。
您可以为 drive1 和 drive2 指定同样的驱动器。

```

# 【24/86】DISKPART
```

Microsoft DiskPart 版本 6.1.7601
Copyright (C) 1999-2008 Microsoft Corporation.
在计算机上: PINGFANGX2

Microsoft DiskPart 语法:
	diskpart [/s <script>] [/?]

	/s <script> - 使用一个 DiskPart 脚本。
	/?          - 显示这个帮助屏幕。

```

# 【25/86】DOSKEY
```
编辑命令行，重新调用 Windows 命令，并创建宏。

DOSKEY [/REINSTALL] [/LISTSIZE=size] [/MACROS[:ALL | :exename]]
  [/HISTORY] [/INSERT | /OVERSTRIKE] [/EXENAME=exename] [/MACROFILE=filename]
  [macroname=[text]]

  /REINSTALL          安装新的 Doskey 副本。
  /LISTSIZE=size      设置命令历史记录的缓冲区大小。
  /MACROS             显示所有 Doskey 宏。
  /MACROS:ALL         为具有 Doskey 宏的所有可执行文件显示
所有 Doskey 宏。
  /MACROS:exename     显示指定可执行文件的所有 Doskey 宏。
  /HISTORY            显示存储在内存中的所有命令。
  /INSERT             指定您键入的新文本插入到旧文本中。
  /OVERSTRIKE         指定新文本覆盖旧文本。
  /EXENAME=exename    指定可执行文件。
  /MACROFILE=filename 指定要安装的宏文件。
  macroname           指定您创建的宏的名称。
  text                指定要录制的命令。

上下箭头 重新调用命令；Esc 清除命令行；F7 
显示命令历史记录；Alt+F7 清除
命令历史记录；F8 搜索命令历史记录；F9 按编号选择命令；Alt+F10 清除宏定义。

以下是 Doskey 宏定义的一些特殊代码:
$T     命令分隔符。允许一个宏中存在多个命令。
$1-$9  批处理参数。与批处理程序中的 %1-%9 等同。
$*     以命令行中命令名称后面的任何内容替换的符号。

```

# 【26/86】DRIVERQUERY
```

DRIVERQUERY [/S system [/U username [/P [password]]]]
              [/FO format] [/NH] [/SI] [/V] 
描述:
    允许管理员显示已安装设备驱动程序
    的列表。

参数列表:
      /S     system           指定要连接到的远程系统。

      /U     [domain\]user    执行命令执行的用户上下文。

      /P     [password]       指定所给用户上下文的密码。

      /FO    format           指定要显示的结果类型。与命令行开关一起传递
                              的有效值是 "TABLE"、"LIST"、" CSV"。

      /NH                     指定“列标题”不应该在屏幕输出中
                              出现。只对 "TABLE" 和 "CSV" 格式有效。

      /SI                     提供有关已签名驱动程序的信息。

      /V                      显示详细任务输出。对签名的驱动程序无效。

      /?                      显示该帮助消息。

示例:
    DRIVERQUERY
    DRIVERQUERY /FO CSV /SI
    DRIVERQUERY /NH
    DRIVERQUERY /S ipaddress /U user /V 
    DRIVERQUERY /S system /U domain\user /P password /FO LIST

```

# 【27/86】ECHO
```
显示信息，或将命令回显打开或关上。

  ECHO [ON | OFF]
  ECHO [message]

要显示当前回显设置，键入不带参数的 ECHO。

```

# 【28/86】ENDLOCAL
```
结束批处理文件中环境改动的本地化操作。在执行ENDLOCAL 之后
所做的环境改动不再仅限于批处理文件。批处理文件结束后，
原先的设置无法还原。

ENDLOCAL

如果命令扩展被启用，ENDLOCAL 会如下改变:

如果相应的 SETLOCAL 用新的 ENABLEEXTENSIONS 或
DISABLEEXTENSIONS 选项启用或停用了命令扩展，那么，在 
ENDLOCAL 之后，命令扩展的启用/停用状态会还原到执行
相应的 SETLOCAL 命令前的状态。

```

# 【29/86】ERASE
```
删除一个或数个文件。

DEL [/P] [/F] [/S] [/Q] [/A[[:]attributes]] names
ERASE [/P] [/F] [/S] [/Q] [/A[[:]attributes]] names

  names         指定一个或多个文件或者目录列表。
                通配符可用来删除多个文件。
                如果指定了一个目录，该目录中的所
                有文件都会被删除。

  /P            删除每一个文件之前提示确认。
  /F            强制删除只读文件。
  /S            删除所有子目录中的指定的文件。
  /Q            安静模式。删除全局通配符时，不要求确认
  /A            根据属性选择要删除的文件
  属性          R  只读文件                     S  系统文件
                H  隐藏文件                     A  存档文件
                I  无内容索引文件               L  重分析点
                -  表示“否”的前缀

如果命令扩展被启用，DEL 和 ERASE 更改如下:

/S 开关的显示句法会颠倒，即只显示已经
删除的文件，而不显示找不到的文件。

```

# 【30/86】EXIT
```
退出 CMD.EXE 程序(命令解释器)或当前批处理脚本。

EXIT [/B] [exitCode]

  /B          指定要退出当前批处理脚本而不是 CMD.EXE。如果从一个
              批处理脚本外执行，则会退出 CMD.EXE

  exitCode    指定一个数字号码。如果指定了 /B，将 ERRORLEVEL
              设成那个数字。如果退出 CMD.EXE，则用那个数字设置
              过程退出代码。

```

# 【31/86】FC
```
比较两个文件或两个文件集并显示它们之间
的不同


FC [/A] [/C] [/L] [/LBn] [/N] [/OFF[LINE]] [/T] [/U] [/W] [/nnnn]
   [drive1:][path1]filename1 [drive2:][path2]filename2
FC /B [drive1:][path1]filename1 [drive2:][path2]filename2

  /A         只显示每个不同处的第一行和最后一行。
  /B         执行二进制比较。
  /C         不分大小写。
  /L         将文件作为 ASCII 文字比较。
  /LBn       将连续不匹配的最大值设置为指定
             的行数。
  /N         在 ASCII 比较上显示行数。
  /OFF[LINE] 不要跳过带有脱机属性集的文件。
  /T         不要将制表符扩充到空格。
  /U         将文件作为 UNICODE 文本文件比较。
  /W         为了比较而压缩空白(制表符和空格)。
  /nnnn      指定不匹配处后必须连续
             匹配的行数。
  [drive1:][path1]filename1
             指定要比较的第一个文件或第一个文件集。
  [drive2:][path2]filename2
             指定要比较的第二个文件或第二个文件集。


```

# 【32/86】FIND
```
在文件中搜索字符串。

FIND [/V] [/C] [/N] [/I] [/OFF[LINE]] "string" [[drive:][path]filename[ ...]]

  /V         显示所有未包含指定字符串的行。
  /C         仅显示包含字符串的行数。
  /N         显示行号。
  /I         搜索字符串时忽略大小写。
  /OFF[LINE] 不要跳过具有脱机属性集的文件。
  "string" 指定要搜索的文本字符串。
  [drive:][path]filename
             指定要搜索的文件。

如果没有指定路径，FIND 将搜索在提示符处键入
的文本或者由另一命令产生的文本。

```

# 【33/86】FINDSTR
```
在文件中寻找字符串。

FINDSTR [/B] [/E] [/L] [/R] [/S] [/I] [/X] [/V] [/N] [/M] [/O] [/P] [/F:file]
        [/C:string] [/G:file] [/D:dir list] [/A:color attributes] [/OFF[LINE]]
        strings [[drive:][path]filename[ ...]]

  /B         在一行的开始配对模式。
  /E         在一行的结尾配对模式。
  /L         按字使用搜索字符串。
  /R         将搜索字符串作为一般表达式使用。
  /S         在当前目录和所有子目录中搜索匹配文件。
  /I         指定搜索不分大小写。
  /X         打印完全匹配的行。
  /V         只打印不包含匹配的行。
  /N         在匹配的每行前打印行数。
  /M         如果文件含有匹配项，只打印其文件名。
  /O         在每个匹配行前打印字符偏移量。
  /P         忽略有不可打印字符的文件。  
  /OFF[LINE] 不跳过带有脱机属性集的文件。
  /A:attr    指定有十六进位数字的颜色属性。请见 "color /?"
  /F:file    从指定文件读文件列表 (/ 代表控制台)。
  /C:string  使用指定字符串作为文字搜索字符串。
  /G:file    从指定的文件获得搜索字符串。 (/ 代表控制台)。
  /D:dir     查找以分号为分隔符的目录列表
  strings    要查找的文字。
  [drive:][path]filename
             指定要查找的文件。

除非参数有 /C 前缀，请使用空格隔开搜索字符串。
例如: 'FINDSTR "hello there" x.y' 在文件 x.y 中寻找 "hello" 或
"there"。'FINDSTR /C:"hello there" x.y' 文件 x.y  寻找
"hello there"。

一般表达式的快速参考:
  .        通配符: 任何字符
  *        重复: 以前字符或类出现零或零以上次数
  ^        行位置: 行的开始
  $        行位置: 行的终点
  [class]  字符类: 任何在字符集中的字符
  [^class] 补字符类: 任何不在字符集中的字符
  [x-y]    范围: 在指定范围内的任何字符
  \x       Escape: 元字符 x 的文字用法
  \<xyz    字位置: 字的开始
  xyz\>    字位置: 字的结束

有关 FINDSTR 常见表达法的详细情况，请见联机命令参考。

```

# 【34/86】FOR
```
对一组文件中的每一个文件执行某个特定命令。

FOR %variable IN (set) DO command [command-parameters]

  %variable  指定一个单一字母可替换的参数。
  (set)      指定一个或一组文件。可以使用通配符。
  command    指定对每个文件执行的命令。
  command-parameters
             为特定命令指定参数或命令行开关。

在批处理程序中使用 FOR 命令时，指定变量请使用 %%variable 
而不要用 %variable。变量名称是区分大小写的，所以 %i 不同于 %I.

如果启用命令扩展，则会支持下列 FOR 命令的其他格式:

FOR /D %variable IN (set) DO command [command-parameters]

    如果集中包含通配符，则指定与目录名匹配，而不与文件名匹配。

FOR /R [[drive:]path] %variable IN (set) DO command [command-parameters]

    检查以 [drive:]path 为根的目录树，指向每个目录中的 FOR 语句。
    如果在 /R 后没有指定目录规范，则使用当前目录。如果集仅为一个单点(.)字符，
    则枚举该目录树。

FOR /L %variable IN (start,step,end) DO command [command-parameters]

    该集表示以增量形式从开始到结束的一个数字序列。因此，(1,1,5)将产生序列
    1 2 3 4 5，(5,-1,1)将产生序列(5 4 3 2 1)

FOR /F ["options"] %variable IN (file-set) DO command [command-parameters]
FOR /F ["options"] %variable IN ("string") DO command [command-parameters]
FOR /F ["options"] %variable IN ('command') DO command [command-parameters]

    或者，如果有 usebackq 选项:

FOR /F ["options"] %variable IN (file-set) DO command [command-parameters]
FOR /F ["options"] %variable IN ("string") DO command [command-parameters]
FOR /F ["options"] %variable IN ('command') DO command [command-parameters]

    fileset 为一个或多个文件名。继续到 fileset 中的下一个文件之前，
    每份文件都被打开、读取并经过处理。处理包括读取文件，将其分成一行行的文字，
    然后将每行解析成零或更多的符号。然后用已找到的符号字符串变量值调用 For 循环。
    以默认方式，/F 通过每个文件的每一行中分开的第一个空白符号。跳过空白行。
    您可通过指定可选 "options" 参数替代默认解析操作。这个带引号的字符串包括一个
    或多个指定不同解析选项的关键字。这些关键字为:

        eol=c           - 指一个行注释字符的结尾(就一个)
        skip=n          - 指在文件开始时忽略的行数。
        delims=xxx      - 指分隔符集。这个替换了空格和跳格键的
                          默认分隔符集。
        tokens=x,y,m-n  - 指每行的哪一个符号被传递到每个迭代
                          的 for 本身。这会导致额外变量名称的分配。m-n
                          格式为一个范围。通过 nth 符号指定 mth。如果
                          符号字符串中的最后一个字符星号，
                          那么额外的变量将在最后一个符号解析之后
                          分配并接受行的保留文本。
        usebackq        - 指定新语法已在下类情况中使用:
                          在作为命令执行一个后引号的字符串并且一个单
                          引号字符为文字字符串命令并允许在 file-set
                          中使用双引号扩起文件名称。

    某些范例可能有助:

FOR /F "eol=; tokens=2,3* delims=, " %i in (myfile.txt) do @echo %i %j %k

    会分析 myfile.txt 中的每一行，忽略以分号打头的那些行，将
    每行中的第二个和第三个符号传递给 for 函数体，用逗号和/或
    空格分隔符号。请注意，此 for 函数体的语句引用 %i 来
    获得第二个符号，引用 %j 来获得第三个符号，引用 %k
    来获得第三个符号后的所有剩余符号。对于带有空格的文件
    名，您需要用双引号将文件名括起来。为了用这种方式来使
    用双引号，还需要使用 usebackq 选项，否则，双引号会
    被理解成是用作定义某个要分析的字符串的。

    %i 在 for 语句中显式声明，%j 和 %k 是通过
    tokens= 选项隐式声明的。可以通过 tokens= 一行
    指定最多 26 个符号，只要不试图声明一个高于字母 "z" 或
    "Z" 的变量。请记住，FOR 变量是单一字母、分大小写和全局的变量；
    而且，不能同时使用超过 52 个。

    还可以在相邻字符串上使用 FOR /F 分析逻辑，方法是，
    用单引号将括号之间的 file-set 括起来。这样，该字符
    串会被当作一个文件中的一个单一输入行进行解析。

    最后，可以用 FOR /F 命令来分析命令的输出。方法是，将
    括号之间的 file-set 变成一个反括字符串。该字符串会
    被当作命令行，传递到一个子 CMD.EXE，其输出会被捕获到
    内存中，并被当作文件分析。如以下例子所示:

      FOR /F "usebackq delims==" %i IN (`set`) DO @echo %i

    会枚举当前环境中的环境变量名称。

另外，FOR 变量参照的替换已被增强。您现在可以使用下列
选项语法:

     %~I          - 删除任何引号(")，扩展 %I
     %~fI        - 将 %I 扩展到一个完全合格的路径名
     %~dI        - 仅将 %I 扩展到一个驱动器号
     %~pI        - 仅将 %I 扩展到一个路径
     %~nI        - 仅将 %I 扩展到一个文件名
     %~xI        - 仅将 %I 扩展到一个文件扩展名
     %~sI        - 扩展的路径只含有短名
     %~aI        - 将 %I 扩展到文件的文件属性
     %~tI        - 将 %I 扩展到文件的日期/时间
     %~zI        - 将 %I 扩展到文件的大小
     %~$PATH:I   - 查找列在路径环境变量的目录，并将 %I 扩展
                   到找到的第一个完全合格的名称。如果环境变量名
                   未被定义，或者没有找到文件，此组合键会扩展到
                   空字符串

可以组合修饰符来得到多重结果:

     %~dpI       - 仅将 %I 扩展到一个驱动器号和路径
     %~nxI       - 仅将 %I 扩展到一个文件名和扩展名
     %~fsI       - 仅将 %I 扩展到一个带有短名的完整路径名
     %~dp$PATH:I - 搜索列在路径环境变量的目录，并将 %I 扩展
                   到找到的第一个驱动器号和路径。
     %~ftzaI     - 将 %I 扩展到类似输出线路的 DIR

在以上例子中，%I 和 PATH 可用其他有效数值代替。%~ 语法
用一个有效的 FOR 变量名终止。选取类似 %I 的大写变量名
比较易读，而且避免与不分大小写的组合键混淆。

```

# 【35/86】FORMAT
```
格式化磁盘以供 Windows 使用。

FORMAT volume [/FS:file-system] [/V:label] [/Q] [/A:size] [/C] [/X] [/P:passes] [/S:state]
FORMAT volume [/V:label] [/Q] [/F:size] [/P:passes]
FORMAT volume [/V:label] [/Q] [/T:tracks /N:sectors] [/P:passes]
FORMAT volume [/V:label] [/Q] [/P:passes]
FORMAT volume [/Q]

  volume          指定驱动器号(后面跟一个冒号)、装入点或卷名。
  /FS:filesystem 指定文件系统的类型(FAT、FAT32、exFAT、NTFS、或 UDF)。
  /V:label        指定卷标。
  /Q              执行快速格式化。请注意，此开关可替代 /P。
  /C              仅适于 NTFS: 默认情况下，将压缩在该新建卷上创建的
                  文件。
  /X              如果必要，请先强制卸除卷。该卷的所有打开句柄
                  不再有效。
  /R:revision     仅 UDF: 强制格式化为特定的 UDF 版本
                  (1.02、1.50、2.00、2.01、2.50)。
                  默认 修订版为 2.01。
  /D              仅适用于 UDF 2.50: 将复制元数据。
  /A:size         替代默认分配单元大小。强烈建议您在通常情况下使用默认 设置。
                  NTFS 支持 512、1024、2048、4096、8192、16K、32K、64K。
                  FAT 支持 512、1024、2048、4096、8192、16K、32K、64k，
                  (128k、256k 用于大于 512 个字节的扇区)。 FAT32 支持 512、
                  1024、2048、4096、8192、16k、32k、64k， (128k 、256k 用于
                  大于 512 个字节的扇区)。EXFAT 支持 512、1024、2048、4096、
                  8192、16K、32K、64K、 128K、256K、512k、1M、2M、4M、8M、16M、
                  32M。

                  请注意，FAT 及 FAT32 文件系统对卷上的群集数量施加以下限制:

                  FAT: 群集数量 <= 65526 FAT32: 65526 < 群集数量 < 4177918

                  如果判定使用指定的群集大小无法满足以上需求，将立即停止格式化。

                  大于 4096 的分配单元大小不支持 NTFS 压缩。

  /F:size 指定要格式化的软盘大小(1.44)
  /T:tracks       为磁盘指定每面磁道数。
  /N:sectors      指定每条磁道的扇区数。
  /P:passes       将卷上每个扇区的操作次数清零。
                  此开关对 /Q 无效
  /S:state        其中 "state" 为 "enable" 或 "disable"
                  默认情况下启用了短名称

```

# 【36/86】FSUTIL
```
/? 是无效参数。
---- 支持的命令 ----

8dot3name       8dot3name 管理
behavior        控制文件系统行为
dirty           管理卷的已损坏位数
file            文件特定命令
fsinfo          文件系统信息
hardlink        硬链接管理
objectid        对象 ID 管理
quota           配额管理
repair          自疗管理
reparsepoint    重分析点管理
resource        事务资源管理器管理
sparse          稀疏文件控制
transaction     事务管理
usn             USN 管理
volume          卷管理

```

# 【37/86】FTYPE
```
显示或修改用在文件扩展名关联中的文件类型

FTYPE [fileType[=[openCommandString]]]

  fileType  指定要检查或改变的文件类型
  openCommandString 指定调用这类文件时要使用的开放式命令。

键入 FTYPE 而不带参数来显示当前有定义的开放式命令字符串的
文件类型。FTYPE 仅用一个文件类型启用时，它显示那个文件类
型目前的开放式命令字符串。如果不为开放式命令字符串指定，
FTYPE 命令将删除那个文件类型的开放式命令字符串。在一个
开放式命令字符串之内，命令字符串 %0 或 %1 被通过关联调用
的文件名所代替。%* 得到所有的参数，%2 得到第一个参数，
%3 得到第二个，等等。%~n 得到其余所有以 nth 参数打头的
参数；n 可以是从 2 到 9 的数字。例如:

    ASSOC .pl=PerlScript
    FTYPE PerlScript=perl.exe %1 %*

允许您启用以下 Perl 脚本:

    script.pl 1 2 3

如果不想键入扩展名，则键入以下字符串:

    set PATHEXT=.pl;%PATHEXT%

被启动的脚本如下:

    script 1 2 3

```

# 【38/86】GOTO
```
将 cmd.exe 定向到批处理程序中带标签的行。

GOTO label

  label   指定批处理程序中用作标签的文字字符串。

标签必须单独一行，并且以冒号打头。

如果命令扩展被启用，GOTO 会如下改变:

GOTO 命令现在接受目标标签 :EOF，这个标签将控制转移到当前
批脚本文件的结尾。不定义就退出批脚本文件，这是一个容易的
办法。有关能使该功能有用的 CALL 命令的扩展描述，请键入
CALL /?。

```

# 【39/86】GPRESULT
```

GPRESULT [/S system [/U username [/P [password]]]] [/SCOPE scope]
           [/USER targetusername] [/R | /V | /Z] [(/X | /H) <filename> [/F]]

描述:
    此命令行工具显示目标用户和计算机的策略结果集 (RSoP) 的信息。

参数列表:
    /S        system           指定要连接到的远程系统。

    /U        [domain\]user    指定命令应在其下执行的
                               用户上下文。
                               无法与 /X、/H 一起使用。

    /P        [password]       为给定的用户上下文指定密码。如果省
                               略则提示输入。
                               无法与 /X、/H 一起使用。

    /SCOPE    scope            指定是显示用户还是计算机设置。
                               有效值: "USER"，"COMPUTER"。

    /USER     [domain\]user    指定要显示 RSOP 的用户名称。



    /X        <filename>       以 XML 格式将报告保存该位置，
                               并使用由
                               <filename> 参数指定的文件名。(在 Windows
                               Vista SP1 和更高版本以及 Windows Server 2008 和更高版本中有效)

    /H        <filename>       以 HTML 格式将报告保存该位置，
                               并使用由
                               <filename> 参数指定的文件名。(在 Windows
                               Vista SP1 和更高版本以及 Windows Server 2008 和更高版本中有效)

    /F                         强制 gpresult 覆盖在
                               /X 或 /H 命令中指定的文件名。

    /R                         显示 RSoP 摘要数据。

    /V                         指定要显示详细信息。详细信息提供
                               已经应用的、优先权是 1 的详细设置。



    /Z                         指定显示超详细信息。超详细信息提供其他
                               详细设置，用 1 或更高的优先权应用于此
                               设置。这允许您查看是否在多处设置了某一
                               设置。请参阅组策略联机帮助主题获得更多
                               信息。




    /?                         显示该帮助消息。


示例:
    GPRESULT /R
    GPRESULT /H GPReport.html
    GPRESULT /USER targetusername /V
    GPRESULT /S system /USER targetusername /SCOPE COMPUTER /Z
    GPRESULT /S system /U username /P password /SCOPE USER /V

```

# 【40/86】GRAFTABL
```

```

# 【41/86】HELP
```
提供 Windows 命令的帮助信息。

HELP [command]

    command - 显示该命令的帮助信息。

```

# 【42/86】ICACLS
```

ICACLS name /save aclfile [/T] [/C] [/L] [/Q]
    将匹配名称的文件和文件夹的 DACL 存储到 aclfile 中以便将来与
    /restore 一起使用。请注意，未保存 SACL、所有者或完整性标签。

ICACLS directory [/substitute SidOld SidNew [...]] /restore aclfile
                 [/C] [/L] [/Q]
    将存储的 DACL 应用于目录中的文件。

ICACLS name /setowner user [/T] [/C] [/L] [/Q]
    更改所有匹配名称的所有者。该选项不会强制更改所有身份；
    使用 takeown.exe 实用程序可实现该目的。

ICACLS name /findsid Sid [/T] [/C] [/L] [/Q]
    查找包含显式提及 SID 的 ACL 的所有匹配名称。

ICACLS name /verify [/T] [/C] [/L] [/Q]
    查找其 ACL 不规范或长度与 ACE 计数不一致的所有文件。

ICACLS name /reset [/T] [/C] [/L] [/Q]
    为所有匹配文件使用默认继承的 ACL 替换 ACL。

ICACLS name [/grant[:r] Sid:perm[...]]
       [/deny Sid:perm [...]]
       [/remove[:g|:d]] Sid[...]] [/T] [/C] [/L]
       [/setintegritylevel Level:policy[...]]

    /grant[:r] Sid:perm 授予指定的用户访问权限。如果使用 :r，
        这些权限将替换以前授予的所有显式权限。
        如果不使用 :r，这些权限将添加到以前授予的所有显式权限。

    /deny Sid:perm 显式拒绝指定的用户访问权限。
        将为列出的权限添加显式拒绝 ACE，
        并删除所有显式授予的权限中的相同权限。

    /remove[:[g|d]] Sid 删除 ACL 中所有出现的 SID。使用
        :g，将删除授予该 SID 的所有权限。使用
        :d，将删除拒绝该 SID 的所有权限。

    /setintegritylevel [(CI)(OI)] 级别将完整性 ACE 显式添加到所有
        匹配文件。要指定的级别为以下级别之一:
            L[ow]
            M[edium]
            H[igh]
        完整性 ACE 的继承选项可以优先于级别，但只应用于
        目录。

    /inheritance:e|d|r
        e - 启用继承
        d - 禁用继承并复制 ACE
        r - 删除所有继承的 ACE


注意:
    Sid 可以采用数字格式或友好的名称格式。如果给定数字格式，
    那么请在 SID 的开头添加一个 *。

    /T 指示在以该名称指定的目录下的所有匹配文件/目录上
        执行此操作。

    /C 指示此操作将在所有文件错误上继续进行。仍将显示错误消息。

    /L 指示此操作在符号链接本身而不是其目标上执行。

    /Q 指示 icacls 应该禁止显示成功消息。

    ICACLS 保留 ACE 项的规范顺序:
            显式拒绝
            显式授予
            继承的拒绝
            继承的授予

    perm 是权限掩码，可以两种格式之一指定:
        简单权限序列:
                N - 无访问权限
                F - 完全访问权限
                M - 修改权限
                RX - 读取和执行权限
                R - 只读权限
                W - 只写权限
                D - 删除权限
        在括号中以逗号分隔的特定权限列表:
                DE - 删除
                RC - 读取控制
                WDAC - 写入 DAC
                WO - 写入所有者
                S - 同步
                AS - 访问系统安全性
                MA - 允许的最大值
                GR - 一般性读取
                GW - 一般性写入
                GE - 一般性执行
                GA - 全为一般性
                RD - 读取数据/列出目录
                WD - 写入数据/添加文件
                AD - 附加数据/添加子目录
                REA - 读取扩展属性
                WEA - 写入扩展属性
                X - 执行/遍历
                DC - 删除子项
                RA - 读取属性
                WA - 写入属性
        继承权限可以优先于每种格式，但只应用于
        目录:
                (OI) - 对象继承
                (CI) - 容器继承
                (IO) - 仅继承
                (NP) - 不传播继承
                (I) - 从父容器继承的权限

示例:

        icacls c:\windows\* /save AclFile /T
        - 将 c:\windows 及其子目录下所有文件的
           ACL 保存到 AclFile。

        icacls c:\windows\ /restore AclFile
        - 将还原 c:\windows 及其子目录下存在的 AclFile 内
          所有文件的 ACL。

        icacls file /grant Administrator:(D,WDAC)
        - 将授予用户对文件删除和写入 DAC 的管理员权限。

        icacls file /grant *S-1-1-0:(D,WDAC)
        - 将授予由 sid S-1-1-0 定义的用户对文件删除和写入 DAC 的权限。

```

# 【43/86】IF
```
执行批处理程序中的条件处理。

IF [NOT] ERRORLEVEL number command
IF [NOT] string1==string2 command
IF [NOT] EXIST filename command

  NOT               指定只有条件为 false 的情况下，Windows 才
                    应该执行该命令。

  ERRORLEVEL number 如果最后运行的程序返回一个等于或大于
                    指定数字的退出代码，指定条件为 true。

  string1==string2  如果指定的文字字符串匹配，指定条件为 true。

  EXIST filename    如果指定的文件名存在，指定条件为 true。

  command           如果符合条件，指定要执行的命令。如果指定的
                    条件为 FALSE，命令后可跟 ELSE 命令，该命令将 
                    在 ELSE 关键字之后执行该命令。

ELSE 子句必须出现在同一行上的 IF 之后。例如:

    IF EXIST filename. (
        del filename.
    ) ELSE (
        echo filename. missing.
    )

由于 del 命令需要用新的一行终止，因此以下子句不会有效:

IF EXIST filename. del filename. ELSE echo filename. missing

由于 ELSE 命令必须与 IF 命令的尾端在同一行上，以下子句也
不会有效:

    IF EXIST filename. del filename.
    ELSE echo filename. missing

如果都放在同一行上，以下子句有效:

    IF EXIST filename. (del filename.) ELSE echo filename. missing

如果命令扩展被启用，IF 会如下改变:

    IF [/I] string1 compare-op string2 command
    IF CMDEXTVERSION number command
    IF DEFINED variable command

其中， compare-op 可以是:

    EQU - 等于
    NEQ - 不等于
    LSS - 小于
    LEQ - 小于或等于
    GTR - 大于
    GEQ - 大于或等于

而 /I 开关(如果指定)说明要进行的字符串比较不分大小写。
/I 开关可以用于 IF 的 string1==string2 的形式上。这些
比较都是通用的；原因是，如果 string1 和 string2 都是
由数字组成的，字符串会被转换成数字，进行数字比较。

CMDEXTVERSION 条件的作用跟 ERRORLEVEL 的一样，除了它
是在跟与命令扩展有关联的内部版本号比较。第一个版本
是 1。每次对命令扩展有相当大的增强时，版本号会增加一个。
命令扩展被停用时，CMDEXTVERSION 条件不是真的。

如果已定义环境变量，DEFINED 条件的作用跟 EXIST 的一样，
除了它取得一个环境变量，返回的结果是 true。

如果没有名为 ERRORLEVEL 的环境变量，%ERRORLEVEL%
会扩充为 ERROLEVEL 当前数值的字符串表达式；否则，您会得到
其数值。运行程序后，以下语句说明 ERRORLEVEL 的用法:

    goto answer%ERRORLEVEL%
    :answer0
    echo Program had return code 0
    :answer1
    echo Program had return code 1

您也可以使用以上的数字比较:

    IF %ERRORLEVEL% LEQ 1 goto okay

如果没有名为 CMDCMDLINE 的环境变量，%CMDCMDLINE%
将在 CMD.EXE 进行任何处理前扩充为传递给 CMD.EXE 的原始
命令行；否则，您会得到其数值。

如果没有名为 CMDEXTVERSION 的环境变量，
%CMDEXTVERSION% 会扩充为 CMDEXTVERSION 当前数值的
字串符表达式；否则，您会得到其数值。

```

# 【44/86】LABEL
```
创建、更改或删除磁盘的卷标。

LABEL [drive:][label]
LABEL [/MP] [volume] [label]

  drive:          指定驱动器号。
  label           指定卷标。
  /MP             指定卷应被视为装入点或卷名。
  volume          指定驱动器号(后面跟一个冒号)、装入点或卷名。
                  如果指定了卷名，/MP 标志则不必要。

```

# 【45/86】MD
```
创建目录。

MKDIR [drive:]path
MD [drive:]path

如果命令扩展被启用，MKDIR 会如下改变:

如果需要，MKDIR 会在路径中创建中级目录。例如: 假设 \a 不
存在，那么:

    mkdir \a\b\c\d

与:

    mkdir \a
    chdir \a
    mkdir b
    chdir b
    mkdir c
    chdir c
    mkdir d

相同。如果扩展被停用，则需要键入 mkdir \a\b\c\d。

```

# 【46/86】MKDIR
```
创建目录。

MKDIR [drive:]path
MD [drive:]path

如果命令扩展被启用，MKDIR 会如下改变:

如果需要，MKDIR 会在路径中创建中级目录。例如: 假设 \a 不
存在，那么:

    mkdir \a\b\c\d

与:

    mkdir \a
    chdir \a
    mkdir b
    chdir b
    mkdir c
    chdir c
    mkdir d

相同。如果扩展被停用，则需要键入 mkdir \a\b\c\d。

```

# 【47/86】MKLINK
```
创建符号链接。

MKLINK [[/D] | [/H] | [/J]] Link Target

        /D      创建目录符号链接。默认为文件
                符号链接。
        /H      创建硬链接，而不是符号链接。
        /J      创建目录联接。
        Link    指定新的符号链接名称。
        Target  指定新链接引用的路径
                (相对或绝对)。

```

# 【48/86】MODE
```
配置系统设备。

串行端口:          MODE COMm[:] [BAUD=b] [PARITY=p] [DATA=d] [STOP=s]
                                [to=on|off] [xon=on|off] [odsr=on|off]
                                [octs=on|off] [dtr=on|off|hs]
                                [rts=on|off|hs|tg] [idsr=on|off]

设备状态:          MODE [device] [/STATUS]

打印重定向:        MODE LPTn[:]=COMm[:]

选择代码页:        MODE CON[:] CP SELECT=yyy

代码页状态:        MODE CON[:] CP [/STATUS]

显示模式:          MODE CON[:] [COLS=c] [LINES=n]

击键率:            MODE CON[:] [RATE=r DELAY=d]

```

# 【49/86】MORE
```
逐屏显示输出。

MORE [/E [/C] [/P] [/S] [/Tn] [+n]] < [drive:][path]filename
command-name | MORE [/E [/C] [/P] [/S] [/Tn] [+n]]
MORE /E [/C] [/P] [/S] [/Tn] [+n] [files]

    [drive:][path]filename  指定要逐屏显示的文件。

    command-name            指定要显示其输出的命令。

    /E      启用扩展功能
    /C      显示页面前先清除屏幕
    /P      扩展 FormFeed 字符
    /S      将多个空白行缩成一行
    /Tn     将制表符扩展为 n 个空格(默认值为 8)

            开关可以出现在 MORE 环境变量中。
    +n      从第 n 行开始显示第一个文件

    files   要显示的文件列表。使用空格分隔列表中的文件。
            如果已启用扩展功能，则在 -- More -- 提示处 接受下列命令:
    P n 显示下 n 行
    S n 跳过下 n 行
    F 显示下个文件
    Q 退出
    = 显示行号
    ? 显示帮助行
    <space> 显示下一页
    <ret> 显示下一行

```

# 【50/86】MOVE
```
移动文件并重命名文件和目录。

要移动至少一个文件:
MOVE [/Y | /-Y] [drive:][path]filename1[,...] destination

要重命名一个目录:
MOVE [/Y | /-Y] [drive:][path]dirname1 dirname2

  [drive:][path]filename1 指定您想移动的文件位置和名称。
  destination             指定文件的新位置。目标可包含一个驱动器号
                          和冒号、一个目录名或组合。如果只移动一个文件
                          并在移动时将其重命名，您还可以包括文件名。
  [drive:][path]dirname1  指定要重命名的目录。
  dirname2                指定目录的新名称。

  /Y                      取消确认覆盖一个现有目标文件的提示。
  /-Y                     对确认覆盖一个现有目标文件发出提示。

命令行开关 /Y 可以出现在 COPYCMD 环境变量中。这可以用命令行上
的 /-Y 替代。默认值是，除非 MOVE 命令是从一个批脚本内
执行的，覆盖时都发出提示。

```

# 【51/86】OPENFILES
```

OPENFILES /parameter [arguments]

描述:
    允许管理员列出或中断系统上已打开的文件和文件夹。

参数列表:
    /Disconnect      中断至少一个打开的文件的连接。

    /Query           显示所有从本地或从共享文件夹打开的文件。

    /Local           启用 / 禁用本地打开文件的显示。

    /?               显示此帮助消息。

示例:
    OPENFILES /Disconnect /?
    OPENFILES /Query /?
    OPENFILES /Local /?

```

# 【52/86】PATH
```
为可执行文件显示或设置一个搜索路径。

PATH [[drive:]path[;...][;%PATH%]
PATH ;

键入 PATH ; 清除所有搜索路径设置并指示 cmd.exe 只在当前
目录中搜索。
键入 PATH 但不加参数，显示当前路径。
将 %PATH% 包括在新的路径设置中会将旧路径附加到新设置。

```

# 【53/86】PAUSE
```
暂停批处理程序，并显示以下消息:
    请按任意键继续. . . 
```

# 【54/86】POPD
```
更改到 PUSHD 命令存储的目录。

POPD


如果命令扩展被启用，从推目录堆栈 POPD 驱动器时，POPD
命令会删除 PUSHD 创建的临时驱动器号。

```

# 【55/86】PRINT
```
打印文本文件。

PRINT [/D:device] [[drive:][path]filename[...]]

   /D:device   指定打印设备。


```

# 【56/86】PROMPT
```
更改 cmd.exe 命令提示符。

PROMPT [text]

  text    指定新的命令提示符。

提示符可以由普通字符及下列特定代码组成:

  $A   & (短 and 符号)
  $B   | (管道)
  $C   ( (左括弧)
  $D   当前日期
  $E   Escape 码(ASCII 码 27)
  $F   ) (右括弧)
  $G   > (大于符号)
  $H   Backspace (擦除前一个字符)
  $L   < (小于符号)
  $N   当前驱动器
  $P   当前驱动器及路径
  $Q   = (等号)
  $S     (空格)
  $T   当前时间
  $V   Windows 版本号
  $_   换行
  $$   $ (货币符号)

如果命令扩展被启用，PROMPT 命令会支持下列格式化字符:

  $+   根据 PUSHD 目录堆栈的深度，零个或零个以上加号(+)字符，
       一个推的层一个字符。

  $M   如果当前驱动器不是网络驱动器，显示跟当前驱动器号或
       空字符串有关联的远程名。

```

# 【57/86】PUSHD
```
保存当前目录以供 POPD 命令使用，然后改到指定的目录。

PUSHD [path | ..]

  path        指定要成为当前目录的目录。

如果命令扩展被启用，除了一般驱动器号和路径，PUSHD 
命令还接受网络路径。如果指定了网络路径，PUSHD 将创建一个
指向指定网络资源的临时驱动器号，然后再用刚定义的驱动器
号更改当前的驱动器和目录。可以从 Z: 往下分配临时驱动器
号，使用找到的第一个没有用过的驱动器号。

```

# 【58/86】RD
```
删除一个目录。

RMDIR [/S] [/Q] [drive:]path
RD [/S] [/Q] [drive:]path

    /S      除目录本身外，还将删除指定目录下的所有子目录和
            文件。用于删除目录树。

    /Q      安静模式，带 /S 删除目录树时不要求确认

```

# 【59/86】RECOVER
```
从损坏的磁盘中恢复可读取的信息。

RECOVER [drive:][path]filename
在使用 RECOVER 命令之前，
请先参阅 Windows 帮助中的联机命令参考。

```

# 【60/86】REM
```
在批处理文件或 CONFIG.SYS 里加上注解或说明。

REM [comment]

```

# 【61/86】REN
```
重命名文件。

RENAME [drive:][path]filename1 filename2.
REN [drive:][path]filename1 filename2.

请注意，您不能为目标文件指定新的驱动器或路径。

```

# 【62/86】RENAME
```
重命名文件。

RENAME [drive:][path]filename1 filename2.
REN [drive:][path]filename1 filename2.

请注意，您不能为目标文件指定新的驱动器或路径。

```

# 【63/86】REPLACE
```
替换文件。

REPLACE [drive1:][path1]filename [drive2:][path2] [/A] [/P] [/R] [/W]
REPLACE [drive1:][path1]filename [drive2:][path2] [/P] [/R] [/S] [/W] [/U]

  [drive1:][path1]filename 指定源文件。
  [drive2:][path2]         指定要替换文件的目录。
  /A                       把新文件加入目标目录。不能和/S 或 /U 命令行开关搭配使用。
  /P                       替换文件或加入源文件之前会先提示您进行确认。
  /R                       替换只读文件以及未受保护的文件。
  /S                       替换目标目录中所有子目录的文件。不能与 /A 命令开关搭配使用。
  /W                       等您插入磁盘以后再运行。
  /U                       只会替换或更新比源文件日期早的文件。不能与 /A 命令行开关搭配使用。

```

# 【64/86】RMDIR
```
删除一个目录。

RMDIR [/S] [/Q] [drive:]path
RD [/S] [/Q] [drive:]path

    /S      除目录本身外，还将删除指定目录下的所有子目录和
            文件。用于删除目录树。

    /Q      安静模式，带 /S 删除目录树时不要求确认

```

# 【65/86】ROBOCOPY
```

-------------------------------------------------------------------------------
   ROBOCOPY     ::     Windows 的可靠文件复制                              
-------------------------------------------------------------------------------

  开始时间: Fri Sep 29 17:07:04 2017

               用法 :: ROBOCOPY source destination [file [file]...] [options]

                 源 :: 源目录(驱动器:\路径或\\服务器\共享\路径)。
               目标 :: 目标目录(驱动器:\路径或\\服务器\共享\路径)。
               文件 :: 要复制的文件(名称/通配符: 默认为 "*.*")。

::
:: 复制选项:
::
                 /S :: 复制子目录，但不复制空的子目录。
                 /E :: 复制子目录，包括空的子目录。
             /LEV:n :: 仅复制源目录树的前 n 层。

                 /Z :: 在可重新启动模式下复制文件。
                 /B :: 在备份模式下复制文件。
                /ZB :: 使用可重新启动模式；如果拒绝访问，请使用备份模式。
            /EFSRAW :: 在 EFS RAW 模式下复制所有加密的文件。

      /COPY:复制标记:: 要复制的文件内容(默认为 /COPY:DAT)。
                       (复制标记: D=数据，A=属性，T=时间戳)。
                       (S=安全=NTFS ACL，O=所有者信息，U=审核信息)。

           /DCOPY:T :: 复制目录时间戳。

               /SEC :: 复制具有安全性的文件(等同于 /COPY:DATS)。
           /COPYALL :: 复制所有文件信息(等同于 /COPY:DATSOU)。
            /NOCOPY :: 不复制任何文件信息(与 /PURGE 一起使用生效)。

            /SECFIX :: 修复所有文件的文件安全性，即使是跳过的文件。
            /TIMFIX :: 修复所有文件的文件时间，即使是跳过的文件。

             /PURGE :: 删除源中不再存在的目标文件/目录。
               /MIR :: 镜像目录树(等同于 /E 和 /PURGE)。

               /MOV :: 移动文件(复制后从源中删除)。
              /MOVE :: 移动文件和目录(复制后从源中删除)。

     /A+:[RASHCNET] :: 将给定的属性添加到复制文件。
     /A-:[RASHCNET] :: 从复制文件中删除给定的属性。

            /CREATE :: 仅创建目录树和长度为零的文件。
               /FAT :: 仅使用 8.3 FAT 文件名创建目标文件。
               /256 :: 关闭超长路径(> 256 字符)支持。

             /MON:n :: 监视源；发现多于 n 个更改时再次运行。
             /MOT:m :: 监视源；如果更改，在 m 分钟时间内再次运行。

      /RH:hhmm-hhmm :: 运行小时数 - 可以启动新副本的时间。
                /PF :: 以每个文件(而不是每个步骤)为基础检查运行小时数。

             /IPG:n :: 程序包间的间距(ms)，以释放低速线路上的带宽。

                /SL :: 对照目标复制符号链接。

            /MT[:n] :: 使用 n 个线程进行多线程复制(默认值为 8)。
                       n 必须至少为 1，但不得大于 128。
                       该选项与 /IPG 和 /EFSRAW 选项不兼容。
                       使用 /LOG 选项重定向输出以便获得最佳性能。

::
:: 文件选择选项:
::
                 /A :: 仅复制具有存档属性集的文件。
                 /M :: 仅复制具有存档属性的文件并重置存档属性。
    /IA:[RASHCNETO] :: 仅包含具有任意给定属性集的文件。
    /XA:[RASHCNETO] :: 排除具有任意给定属性集的文件。

  /XF 文件[文件]... :: 排除与给定名称/路径/通配符匹配的文件。
  /XD 目录[目录]... :: 排除与给定名称/路径匹配的目录。

                /XC :: 排除已更改的文件。
                /XN :: 排除较新的文件。
                /XO :: 排除较旧的文件。
                /XX :: 排除多余的文件和目录。
                /XL :: 排除孤立的文件和目录。
                /IS :: 包含相同文件。
                /IT :: 包含已调整的文件。

             /MAX:n :: 最大的文件大小 - 排除大于 n 字节的文件。
             /MIN:n :: 最小的文件大小 - 排除小于 n 字节的文件。

          /MAXAGE:n :: 最长的文件存在时间 - 排除早于 n 天/日期的文件。
          /MINAGE:n :: 最短的文件存在时间 - 排除晚于 n 天/日期的文件。
          /MAXLAD:n :: 最大的最后访问日期 - 排除自 n 以来未使用的文件。
          /MINLAD:n :: 最小的最后访问日期 - 排除自 n 以来使用的文件。
                       (If n < 1900 then n = n days, else n = YYYYMMDD date)。

                /XJ :: 排除接合点。(默认情况下通常包括)。

               /FFT :: 假设 FAT 文件时间(2 秒粒度)。
               /DST :: 弥补 1 小时的 DST 时间差。

               /XJD :: 排除目录的接合点。
               /XJF :: 排除文件的接合点。

::
:: 重试选项:
::
               /R:n :: 失败副本的重试次数: 默认为 1 百万。
               /W:n :: 两次重试间的等待时间: 默认为 30 秒。

               /REG :: 将注册表中的 /R:n 和 /W:n 保存为默认设置。

               /TBD :: 等待定义共享名称(重试错误 67)。

::
:: 日志记录选项:
::
                 /L :: 仅列出 - 不复制、添加时间戳或删除任何文件。
                 /X :: 报告所有多余的文件，而不只是选中的文件。
                 /V :: 生成详细输出，同时显示跳过的文件。
                /TS :: 在输出中包含源文件的时间戳。
                /FP :: 在输出中包含文件的完整路径名称。
             /BYTES :: 以字节打印大小。

                /NS :: 无大小 - 不记录文件大小。
                /NC :: 无类别 - 不记录文件类别。
               /NFL :: 无文件列表 - 不记录文件名。
               /NDL :: 无目录列表 - 不记录目录名称。

                /NP :: 无进度 - 不显示已复制的百分比。
               /ETA :: 显示复制文件的预期到达时间。

          /LOG:文件 :: 将状态输出到日志文件(覆盖现有日志)。
         /LOG+:文件 :: 将状态输出到日志文件(附加到现有日志中)。

       /UNILOG:文件 :: 以 UNICODE 方式将状态输出到日志文件(覆盖现有日志)。
      /UNILOG+:文件 :: 以 UNICODE 方式将状态输出到日志文件(附加到现有日志中)。

               /TEE :: 输出到控制台窗口和日志文件。

               /NJH :: 没有作业标头。
               /NJS :: 没有作业摘要。

           /UNICODE :: 以 UNICODE 方式输出状态。

::
:: 作业选项 :
::
      /JOB:作业名称 :: 从命名的作业文件中提取参数。
     /SAVE:作业名称 :: 将参数保存到命名的作业文件
              /QUIT :: 处理命令行后退出(以查看参数)。 
              /NOSD :: 未指定源目录。
              /NODD :: 未指定目标目录。
                /IF :: 包含以下文件。

```

# 【66/86】SET
```
显示、设置或删除 cmd.exe 环境变量。

SET [variable=[string]]

  variable  指定环境变量名。
  string    指定要指派给变量的一系列字符串。

要显示当前环境变量，键入不带参数的 SET。

如果命令扩展被启用，SET 会如下改变:

可仅用一个变量激活 SET 命令，等号或值不显示所有前缀匹配
SET 命令已使用的名称的所有变量的值。例如:

    SET P

会显示所有以字母 P 打头的变量

如果在当前环境中找不到该变量名称，SET 命令将把 ERRORLEVEL
设置成 1。

SET 命令不允许变量名含有等号。

在 SET 命令中添加了两个新命令行开关:

    SET /A expression
    SET /P variable=[promptString]

/A 命令行开关指定等号右边的字符串为被评估的数字表达式。该表达式
评估器很简单并以递减的优先权顺序支持下列操作:

    ()                  - 分组
    ! ~ -               - 一元运算符
    * / %               - 算数运算符
    + -                 - 算数运算符
    << >>               - 逻辑移位
                       - 按位“与”
    ^                   - 按位“异”
    |                   - 按位“或”
    = *= /= %= += -=    - 赋值
      &= ^= |= <<= >>=
    ,                   - 表达式分隔符

如果您使用任何逻辑或取余操作符， 您需要将表达式字符串用
引号扩起来。在表达式中的任何非数字字符串键作为环境变量
名称，这些环境变量名称的值已在使用前转换成数字。如果指定
了一个环境变量名称，但未在当前环境中定义，那么值将被定为
零。这使您可以使用环境变量值做计算而不用键入那些 % 符号
来得到它们的值。如果 SET /A 在命令脚本外的命令行执行的，
那么它显示该表达式的最后值。该分配的操作符在分配的操作符
左边需要一个环境变量名称。除十六进制有 0x 前缀，八进制
有 0 前缀的，数字值为十进位数字。因此，0x12 与 18 和 022 
相同。请注意八进制公式可能很容易搞混: 08 和 09 是无效的数字，
因为 8 和 9 不是有效的八进制位数。(& )

/P 命令行开关允许将变量数值设成用户输入的一行输入。读取输入
行之前，显示指定的 promptString。promptString 可以是空的。

环境变量替换已如下增强:

    %PATH:str1=str2%

会扩展 PATH 环境变量，用 "str2" 代替扩展结果中的每个 "str1"。
要有效地从扩展结果中删除所有的 "str1"，"str2" 可以是空的。
"str1" 可以以星号打头；在这种情况下，"str1" 会从扩展结果的
开始到 str1 剩余部分第一次出现的地方，都一直保持相配。

也可以为扩展名指定子字符串。

    %PATH:~10,5%

会扩展 PATH 环境变量，然后只使用在扩展结果中从第 11 个(偏
移量 10)字符开始的五个字符。如果没有指定长度，则采用默认
值，即变量数值的余数。如果两个数字(偏移量和长度)都是负数，
使用的数字则是环境变量数值长度加上指定的偏移量或长度。

    %PATH:~-10%

会提取 PATH 变量的最后十个字符。

    %PATH:~0,-2%

会提取 PATH 变量的所有字符，除了最后两个。

终于添加了延迟环境变量扩充的支持。该支持总是按默认值被
停用，但也可以通过 CMD.EXE 的 /V 命令行开关而被启用/停用。
请参阅 CMD /?

考虑到读取一行文本时所遇到的目前扩充的限制时，延迟环境
变量扩充是很有用的，而不是执行的时候。以下例子说明直接
变量扩充的问题:

    set VAR=before
    if "%VAR%" == "before" (
        set VAR=after
        if "%VAR%" == "after" @echo If you see this, it worked
    )

不会显示消息，因为在读到第一个 IF 语句时，BOTH IF 语句中
的 %VAR% 会被代替；原因是: 它包含 IF 的文体，IF 是一个
复合语句。所以，复合语句中的 IF 实际上是在比较 "before" 和
"after"，这两者永远不会相等。同样，以下这个例子也不会达到
预期效果:

    set LIST=
    for %i in (*) do set LIST=%LIST% %i
    echo %LIST%

原因是，它不会在目前的目录中建立一个文件列表，而只是将
LIST 变量设成找到的最后一个文件。这也是因为 %LIST% 在
FOR 语句被读取时，只被扩充了一次；而且，那时的 LIST 变量
是空的。因此，我们真正执行的 FOR 循环是:

    for %i in (*) do set LIST= %i

这个循环继续将 LIST 设成找到的最后一个文件。

延迟环境变量扩充允许您使用一个不同的字符(惊叹号)在执行
时间扩充环境变量。如果延迟的变量扩充被启用，可以将上面
例子写成以下所示，以达到预期效果:

    set VAR=before
    if "%VAR%" == "before" (
        set VAR=after
        if "!VAR!" == "after" @echo If you see this, it worked
    )

    set LIST=
    for %i in (*) do set LIST=!LIST! %i
    echo %LIST%

如果命令扩展被启用，有几个动态环境变量可以被扩展，但不会出现在 SET 显示的变
量列表中。每次变量数值被扩展时，这些变量数值都会被动态计算。如果用户用这些
名称中任何一个明确定义变量，那个定义会替代下面描述的动态定义:

%CD% - 扩展到当前目录字符串。

%DATE% - 用跟 DATE 命令同样的格式扩展到当前日期。

%TIME% - 用跟 TIME 命令同样的格式扩展到当前时间。

%RANDOM% - 扩展到 0 和 32767 之间的任意十进制数字。

%ERRORLEVEL% - 扩展到当前 ERRORLEVEL 数值。

%CMDEXTVERSION% - 扩展到当前命令处理器扩展版本号。

%CMDCMDLINE% - 扩展到调用命令处理器的原始命令行。

%HIGHESTNUMANODENUMBER% - 扩展到此计算机上的最高 NUMA 节点号。

```

# 【67/86】SETLOCAL
```
开始批处理文件中环境改动的本地化操作。在执行 SETLOCAL 之后
所做的环境改动只限于批处理文件。要还原原先的设置，必须执
行 ENDLOCAL。达到批处理文件结尾时，对于该批处理文件的每个
尚未执行的 SETLOCAL 命令，都会有一个隐含的 ENDLOCAL 被执行。

SETLOCAL

如果命令扩展被启用，SETLOCAL 会如下改变:

SETLOCAL 批命令现在可以接受可选参数:
        ENABLEEXTENSIONS / DISABLEEXTENSIONS
            启用或禁用命令处理器扩展。这些
            参数比 CMD /E:ON 或 /E:OFF
            开关有优先权。请参阅 CMD /? 获取详细信息。
        ENABLEDELAYEDEXPANSION / DISABLEDELAYEDEXPANSION
            启用或禁用延缓环境变量
            扩展。这些参数比 CMD
            /V:ON 或 /V:OFF 开关有优先权。请参阅 CMD /? 获取详细信息。
无论在 SETLOCAL 命令之前它们的设置是什么，这些修改会一直
保留到匹配的 ENDLOCAL 命令。

如果有一个参数，
SETLOCAL 命令将设置 ERRORLEVEL 的值。如果有两个有效参数中的一个，
该值则为零。
用下列技巧，您可以在批脚本中
使用这个来决定扩展是否可用:

    VERIFY OTHER 2>nul
    SETLOCAL ENABLEEXTENSIONS
    IF ERRORLEVEL 1 echo Unable to enable extensions

这个方法之所以有效，是因为在 CMD.EXE 的旧版本上，SETLOCAL
未设置 ERRORLEVEL 值。具有不正确参数的 VERIFY 命令将
ERRORLEVEL 值初始化成非零值。

```

# 【68/86】SC


# 【69/86】SCHTASKS
```

SCHTASKS /parameter [arguments] 

描述:
    允许管理员创建、删除、查询、更改、运行和中止本地或远程系统上的计划任
    务。

参数列表:
    /Create         创建新计划任务。

    /Delete         删除计划任务。

    /Query          显示所有计划任务。

    /Change         更改计划任务属性。

    /Run            按需运行计划任务。

    /End            中止当前正在运行的计划任务。

    /ShowSid        显示与计划的任务名称相应的安全标识符。

    /?              显示此帮助消息。

Examples:
    SCHTASKS 
    SCHTASKS /?
    SCHTASKS /Run /?
    SCHTASKS /End /?
    SCHTASKS /Create /?
    SCHTASKS /Delete /?
    SCHTASKS /Query  /?
    SCHTASKS /Change /?
    SCHTASKS /ShowSid /?

```

# 【70/86】SHIFT
```
更改批处理文件中可替换参数的位置。

SHIFT [/n]

如果命令扩展被启用，SHIFT 命令支持/n 命令行开关；该命令行开关告诉
命令从第 n 个参数开始移位；n 介于零和八之间。例如:

    SHIFT /2

会将 %3 移位到 %2，将 %4 移位到 %3，等等；并且不影响 %0 和 %1。

```

# 【71/86】SHUTDOWN
```
用法: SHUTDOWN [/i | /l | /s | /r | /g | /a | /p | /h | /e] [/f]
    [/m \\computer][/t xxx][/d [p|u:]xx:yy [/c "comment"]]

    没有参数   显示帮助。这与键入 /? 是一样的。
    /?         显示帮助。这与不键入任何选项是一样的。
    /i         显示图形用户界面(GUI)。
               这必须是第一个选项。
    /l         注销。这不能与 /m 或 /d 选项一起使用。
    /s         关闭计算机。
    /r         关闭并重新启动计算机。
    /g         关闭并重新启动计算机。系统重新启动后，
               重新启动所有注册的应用程序。
    /a         中止系统关闭。
               这只能在超时期间使用。
    /p         关闭本地计算机，没有超时或警告。
               可以与 /d 和 /f 选项一起使用。
    /h         休眠本地计算机。
               可以与 /f 选项一起使用。
    /e         记录计算机意外关闭的原因。
    /m \\computer 指定目标计算机。
    /t xxx     设置关闭前的超时为 xxx 秒。
               有效范围是 0-315360000 (10 年)，默认值为 30。
               如果超时时间大于 0，则默示 /f 
               参数。
    /c "comment" 重启动或关闭的原因的注释。
               最多允许 512 个字符。
    /f         强制正在运行的应用程序关闭，不前台警告用户。
               当为 /t 参数指定大于 0 的值时，
               则默示 /f 参数。
    /d [p|u:]xx:yy  提供重新启动或关机的原因。
               p 表明重新启动或关闭是计划内的。
               u 表示原因由用户定义。
               如果 p 和 u 均未指定，则是计划外重新启动
               或关闭。
               xx 是主要原因号(小于 256 的正整数)。
               yy 是次要原因号(小于 65536 的正整数)。

此计算机上的原因:
(E = 预期 U = 意外 P = 计划内，C = 自定义)
类别	主要 	次要	标题

 U  	0	0	其他(计划外)
E   	0	0	其他(计划外)
E P 	0	0	其他(计划内)
 U  	0	5	其他故障: 系统没有反应
E   	1	1	硬件: 维护(计划外)
E P 	1	1	硬件: 维护(计划内)
E   	1	2	硬件: 安装(计划外)
E P 	1	2	硬件: 安装(计划内)
E   	2	2	操作系统: 恢复(计划内)
E P 	2	2	操作系统: 恢复(计划内)
  P 	2	3	操作系统: 升级(计划内)
E   	2	4	操作系统: 重新配置(计划外)
E P 	2	4	操作系统: 重新配置(计划内)
  P 	2	16	操作系统: Service Pack (计划内)
    	2	17	操作系统: 热修补(计划外)
  P 	2	17	操作系统: 热修补(计划内)
    	2	18	操作系统: 安全修补(计划外)
  P 	2	18	操作系统: 安全修补(计划内)
E   	4	1	应用程序: 维护(计划外)
E P 	4	1	应用程序: 维护(计划内)
E P 	4	2	应用程序: 安装(计划内)
E   	4	5	应用程序: 没有反应
E   	4	6	应用程序: 不稳定
 U  	5	15	系统故障: 停止错误
 U  	5	19	
E   	5	19	
E P 	5	19	
E   	5	20	网络连接丢失(计划外)
 U  	6	11	电源故障: 电线被拔掉
 U  	6	12	电源故障: 环境
  P 	7	0	旧版 API 关机

```

# 【72/86】SORT
```
SORT [/R] [/+n] [/M kilobytes] [/L locale] [/REC recordbytes]

  [[drive1:][path1]filename1] [/T [drive2:][path2]]

  [/O [drive3:][path3]filename3]

  /+n                         指定开始每个比较的字符号码 n。/+3 说明每个

                              比较应从每行的第三个字符开始。少于 n 个字符

                              的行排在其他行之前。按默认值，从每行的第一

                              个字符开始比较。

  /L[OCALE] locale            用指定的区域设置替代系统默认区域设置。

                              ""C"" 区域设置产生最快的排序顺序并且是当前

                              的唯一其他选择。排序总是不分大小写的。

  /M[EMORY] kilobytes         指定用于排序的主内存量，单位为 KB。

                              最小内存量总是 160 KB。如果指定内存大小，

                              无论主内存的可用量是多少，指定的内存量会

                              全部用于排序。



                              要取得最佳性能，通常不指定内存大小。按默认

                              值，如果达到默认最大内存值，排序会一次完成

                              (非临时文件)；否则，排序会分两次完成(没有

                              完全排序的数据存储在临时文件中)；用于排序

                              和合并的内存量相等。如果输入和输出都是文

                              件，默认最大内存量为可用主内存的 90%;

                              否则，为主内存的 45%。

  /REC[ORD_MAXIMUM] characters 指定记录中的最大字符数量

                              (默认值为 4096，最大值为 65535)。

  /R[EVERSE]                  颠倒排序顺序，即，从 Z 到 A，再从 9 到 0。

  [drive1:][path1]filename1   指定要排序的文件。如果没有指定，则排序标准

                              输入。指定输入文件比将同一个文件重定向为标

                              准输入快。

  /T[EMPORARY]

    [drive2:][path2]          指定保留排序工作存储的目录路径，以防主内

                              存无法容纳数据。默认值是使用系统临时目录。

  /O[UTPUT]

    [drive3:][path3]filename3 指定在哪个文件中储存经过排序的输入。

                              如果没有指定，数据会被写入标准输出。指定

                              输出文件比将标准输出重定向到同一个文件快。



```

# 【73/86】START
```
启动一个单独的窗口运行指定的程序或命令。

START ["title"] [/D path] [/I] [/MIN] [/MAX] [/SEPARATE | /SHARED]
      [/LOW | /NORMAL | /HIGH | /REALTIME | /ABOVENORMAL | /BELOWNORMAL]
      [/NODE <NUMA node>] [/AFFINITY <hex affinity mask>] [/WAIT] [/B]
      [command/program] [parameters]

    "title"     在窗口标题栏中显示的标题。
    path        启动目录。
    B           启动应用程序，但不创建新窗口。应用程序已忽略 ^C 处理。
                除非应用程序启用 ^C 处理，否则 ^Break 是唯一可以中断
                该应用程序的方式。
    I           新的环境将是传递给 cmd.exe 的原始环境，而不是当前环境。                
    MIN         以最小化方式启动窗口。
    MAX         以最大化方式启动窗口。
    SEPARATE    在单独的内存空间中启动 16 位 Windows 程序。
    SHARED      在共享内存空间中启动 16 位 Windows 程序。
    LOW         在 IDLE 优先级类中启动应用程序。
    NORMAL      在 NORMAL 优先级类中启动应用程序。
    HIGH        在 HIGH 优先级类中启动应用程序。
    REALTIME    在 REALTIME 优先级类中启动应用程序。
    ABOVENORMAL 在 ABOVENORMAL 优先级类中启动应用程序。
    BELOWNORMAL 在 BELOWNORMAL 优先级类中启动应用程序。
    NODE        将首选非一致性内存结构 (NUMA) 节点指定为十进制整数。
    AFFINITY    将处理器关联掩码指定为十六进制数字。进程被限制在这些
                处理器上运行。

                当 /AFFINITY 和 /NODE 结合时，会对关联掩码进行不同的解释。
                指定关联掩码，正如 NUMA 节点的处理器掩码正确移动到零位
                起始位置一样。进程被限制在指定关联掩码和 NUMA 节点之间的
                那些通用处理器上运行。如果没有通用处理器，则进程被限制在
                指定的 NUMA 节点上运行。
    WAIT        启动应用程序并等待它终止。
    command/program
                如果它是内部 cmd 命令或批文件，则该命令处理器是使用
                cmd.exe 的 /K 开关运行的。这表示运行该命令之后，该窗口
                将仍然存在。

                如果它不是内部 cmd 命令或批文件，则它就是一个程序，并将
                作为一个窗口化应用程序或控制台应用程序运行。

    parameters  这些是传递给 command/program 的参数。

注意: 在 64 位平台上不支持 SEPARATE 和 SHARED 选项。

通过指定 /NODE，可按照利用 NUMA 系统中的内存区域的方式创建进程。例如，
可以创建两个完全通过共享内存互相通信的进程以共享相同的首选 NUMA 节点，
从而最大限度地减少内存延迟。如有可能，它们即会分配来自相同 NUMA 节点的
内存，并且会在指定节点之外的处理器上自由运行。

    启动 /NODE 1 application1.exe
    启动 /NODE 1 application2.exe

这两个进程可被进一步限制在相同 NUMA 节点内的指定处理器上运行。在以下
示例中， application1 在节点的两个低顺序处理器上运行，而 application2
在该节点的其后两个处理器上运行。该示例假定指定节点至少具有四个逻辑
处理器。请注意，节点号可更改为该计算机的任何有效节点号，而无需更改关联
掩码。

    启动 /NODE 1 /AFFINITY 0x3 application1.exe
    启动 /NODE 1 /AFFINITY 0xc application2.exe

如果命令扩展被启用，通过命令行或 START 命令的外部命令
调用会如下改变:

将文件名作为命令键入，非可执行文件可以通过文件关联调用。
    (例如，WORD.DOC 会调用跟 .DOC 文件扩展名关联的应用程序)。
    关于如何从命令脚本内部创建这些关联，请参阅 ASSOC 和
     FTYPE 命令。

执行的应用程序是 32-位 GUI 应用程序时，CMD.EXE 不等应用
    程序终止就返回命令提示符。如果在命令脚本内执行，该新行为
    则不会发生。

如果执行的命令行的第一个符号是不带扩展名或路径修饰符的
    字符串 "CMD"，"CMD" 会被 COMSPEC 变量的数值所替换。这
    防止从当前目录提取 CMD.EXE。

如果执行的命令行的第一个符号没有扩展名，CMD.EXE 会使用
    PATHEXT 环境变量的数值来决定要以什么顺序寻找哪些扩展
    名。PATHEXT 变量的默认值是:

        .COM;.EXE;.BAT;.CMD

    请注意，该语法跟 PATH 变量的一样，分号隔开不同的元素。

查找可执行文件时，如果没有相配的扩展名，看一看该名称是否
与目录名相配。如果确实如此，START 会在那个路径上调用 
Explorer。如果从命令行执行，则等同于对那个路径作 CD /D。

```

# 【74/86】SUBST
```
将路径与驱动器号关联。

SUBST [drive1: [drive2:]path]
SUBST drive1: /D

  drive1:        指定要分配路径的虚拟驱动器。
  [drive2:]path  指定物理驱动器和要分配给虚拟驱动器的路径。
  /D             删除被替换的
(虚拟)驱动器。

不带参数键入 SUBST，以显示当前虚拟驱动器的列表。

```

# 【75/86】SYSTEMINFO
```

SYSTEMINFO [/S system [/U username [/P [password]]]] [/FO format] [/NH]

描述:
    该工具显示本地或远程机器(包括服务包级别)的操作系统配置的信息。

参数列表:
    /S      system           指定要连接的远程系统。

    /U      [domain\]user    指定应该在哪个用户上下文执行命令。


    /P      [password]       指定给定用户上下文的密码。如果省略则
                             提示输入。

    /FO     format           指定显示结果的格式。
                             有效值: "TABLE"、"LIST"、"CSV"。

    /NH                      指定“列标题”不应该在输出中显示。
                             只对 "TABLE" 和 "CSV" 格式有效。

    /?                       显示帮助消息。


例如:
    SYSTEMINFO
    SYSTEMINFO /?
    SYSTEMINFO /S system
    SYSTEMINFO /S system /U user
    SYSTEMINFO /S system /U domain\user /P password /FO TABLE
    SYSTEMINFO /S system /FO LIST
    SYSTEMINFO /S system /FO CSV /NH

```

# 【76/86】TASKLIST
```

TASKLIST [/S system [/U username [/P [password]]]]
         [/M [module] | /SVC | /V] [/FI filter] [/FO format] [/NH]

描述:
    该工具显示在本地或远程机器上当前运行的进程列表。

参数列表:
   /S     system           指定连接到的远程系统。

   /U     [domain\]user    指定应该在哪个用户上下文执行这个命令。

   /P     [password]       为提供的用户上下文指定密码。如果省略，则
                           提示输入。

   /M     [module]         列出当前使用所给 exe/dll 名称的所有任务。
                           如果没有指定模块名称，显示所有加载的模块。

   /SVC                    显示每个进程中主持的服务。

   /V                      显示详述任务信息。

   /FI    filter           显示一系列符合筛选器指定的标准的任务。

   /FO    format           指定输出格式。
                           有效值: "TABLE"、"LIST"、"CSV"。

   /NH                     指定列标题不应该在输出中显示。
                           只对 "TABLE" 和 "CSV" 格式有效。

   /?                      显示帮助消息。


筛选器:
    筛选器名        有效操作符                有效值
    -----------     ---------------           --------------------------
    STATUS          eq, ne                    RUNNING | 
                                              NOT RESPONDING | UNKNOWN
    IMAGENAME       eq, ne                    映像名称
    PID             eq, ne, gt, lt, ge, le    PID 值
    SESSION         eq, ne, gt, lt, ge, le    会话编号
    SESSIONNAME     eq, ne                    会话名
    CPUTIME         eq, ne, gt, lt, ge, le    CPU 时间，格式为
                                              hh:mm:ss。
                                              hh - 时，
                                              mm - 分，ss - 秒
    MEMUSAGE        eq, ne, gt, lt, ge, le    内存使用量，单位为 KB
    USERNAME        eq, ne                    用户名，格式为 [domain\]user
    SERVICES        eq, ne                    服务名称
    WINDOWTITLE     eq, ne                    窗口标题
    MODULES         eq, ne                    DLL 名称

说明: 当查询远程机器时，不支持 "WINDOWTITLE" 和 "STATUS"
      筛选器。

示例:
    TASKLIST
    TASKLIST /M
    TASKLIST /V /FO CSV
    TASKLIST /SVC /FO LIST
    TASKLIST /M wbem*
    TASKLIST /S system /FO LIST
    TASKLIST /S system /U domain\username /FO CSV /NH
    TASKLIST /S system /U username /P password /FO TABLE /NH
    TASKLIST /FI "USERNAME ne NT AUTHORITY\SYSTEM" /FI "STATUS eq running"

```

# 【77/86】TASKKILL
```

TASKKILL [/S system [/U username [/P [password]]]]
         { [/FI filter] [/PID processid | /IM imagename] } [/T] [/F]

描述:
    使用该工具按照进程 ID (PID) 或映像名称终止任务。

参数列表:
    /S    system           指定要连接的远程系统。

    /U    [domain\]user    指定应该在哪个用户上下文执行这个命令。

    /P    [password]       为提供的用户上下文指定密码。如果忽略，提示
                           输入。

    /FI   filter           应用筛选器以选择一组任务。
                           允许使用 "*"。例如，映像名称 eq acme*

    /PID  processid        指定要终止的进程的 PID。
                           使用 TaskList 取得 PID。

    /IM   imagename        指定要终止的进程的映像名称。通配符 '*'可用来
                           指定所有任务或映像名称。

    /T                     终止指定的进程和由它启用的子进程。

    /F                     指定强制终止进程。

    /?                     显示帮助消息。

筛选器:
    筛选器名      有效运算符                有效值
    -----------   ---------------           -------------------------
    STATUS        eq, ne                    RUNNING |
                                            NOT RESPONDING | UNKNOWN
    IMAGENAME     eq, ne                    映像名称
    PID           eq, ne, gt, lt, ge, le    PID 值
    SESSION       eq, ne, gt, lt, ge, le    会话编号。
    CPUTIME       eq, ne, gt, lt, ge, le    CPU 时间，格式为
                                            hh:mm:ss。
                                            hh - 时，
                                            mm - 分，ss - 秒
    MEMUSAGE      eq, ne, gt, lt, ge, le    内存使用量，单位为 KB
    USERNAME      eq, ne                    用户名，格式为 [domain\]user
    MODULES       eq, ne                    DLL 名称
    SERVICES      eq, ne                    服务名称
    WINDOWTITLE   eq, ne                    窗口标题

    说明
    ----
    1) 只有在应用筛选器的情况下，/IM 切换才能使用通配符 '*'。
    2) 远程进程总是要强行 (/F) 终止。
    3) 当指定远程机器时，不支持 "WINDOWTITLE" 和 "STATUS" 筛选器。

例如:
    TASKKILL /IM notepad.exe
    TASKKILL /PID 1230 /PID 1241 /PID 1253 /T
    TASKKILL /F /IM cmd.exe /T 
    TASKKILL /F /FI "PID ge 1000" /FI "WINDOWTITLE ne untitle*"
    TASKKILL /F /FI "USERNAME eq NT AUTHORITY\SYSTEM" /IM notepad.exe
    TASKKILL /S system /U domain\username /FI "USERNAME ne NT*" /IM *
    TASKKILL /S system /U username /P password /FI "IMAGENAME eq note*"

```

# 【78/86】TIME
```
显示或设置系统时间。

TIME [/T | time]

显示当前时间设置和输入新时间的提示，请键入
不带参数的 TIME。要保留现有时间，请按 Enter。

如果命令扩展被启用，TIME 命令会支持 /T 命令行开关；该命令行开关告诉
命令只输出当前时间，但不提示输入新时间。

```

# 【79/86】TITLE
```
设置命令提示窗口的窗口标题。

TITLE [string]

  string       指定命令提示窗口的标题。

```

# 【80/86】TREE
```
以图形显示驱动器或路径的文件夹结构。

TREE [drive:][path] [/F] [/A]

   /F   显示每个文件夹中文件的名称。
   /A   使用 ASCII 字符，而不使用扩展字符。


```

# 【81/86】TYPE
```
显示文本文件的内容。

TYPE [drive:][path]filename

```

# 【82/86】VER
```
显示 Windows 版本。

VER

```

# 【83/86】VERIFY
```
指示 cmd.exe 是否要验证文件是否已正确地写入磁盘。
  
VERIFY [ON | OFF]

要显示当前 VERIFY 设置，键入不带参数的 VERIFY。

```

# 【84/86】VOL
```
显示磁盘卷标和序列号(如果存在)。

VOL [drive:]

```

# 【85/86】XCOPY
```
复制文件和目录树。

XCOPY source [destination] [/A | /M] [/D[:date]] [/P] [/S [/E]] [/V] [/W]
                           [/C] [/I] [/Q] [/F] [/L] [/G] [/H] [/R] [/T] [/U]
                           [/K] [/N] [/O] [/X] [/Y] [/-Y] [/Z] [/B]
                           [/EXCLUDE:file1[+file2][+file3]...]

  source       指定要复制的文件。
  destination  指定新文件的位置和/或名称。
  /A           仅复制有存档属性集的文件，但不更改属性。
  /M           仅复制有存档属性集的文件，并关闭存档属性。
  /D:m-d-y     复制在指定日期或指定日期以后更改的文件。
               如果没有提供日期，只复制那些源时间比目标时间新的文件。
  /EXCLUDE:file1[+file2][+file3]...
               指定含有字符串的文件列表。每个字符串在文件中应位于单独的一行。
               如果任何字符串与复制文件的绝对路径的任何部分相符，则排除复制
               该文件。例如，指定如 \obj\ 或 .obj 的字符串会分别排除目录
               obj 下面的所有文件或带有 .obj 扩展名的所有文件。
  /P           创建每个目标文件之前提示您。
  /S           复制目录和子目录，不包括空目录。
  /E           复制目录和子目录，包括空目录。与 /S /E 相同。可以用来修改 /T。
  /V           验证每个新文件的大小。
  /W           提示您在复制前按键。
  /C           即使有错误，也继续复制。
  /I           如果目标不存在，且要复制多个文件，则假定目标必须是目录。
  /Q           复制时不显示文件名。
  /F           复制时显示完整的源文件名和目标文件名。
  /L           显示要复制的文件。
  /G           允许将加密文件复制到不支持加密的目标。
  /H           也复制隐藏文件和系统文件。
  /R           覆盖只读文件。
  /T           创建目录结构，但不复制文件。不包括空目录或子目录。/T /E 包括
               空目录和子目录。
  /U           只复制已经存在于目标中的文件。
  /K           复制属性。一般的 Xcopy 会重设只读属性。
  /N           用生成的短名称复制。
  /O           复制文件所有权和 ACL 信息。
  /X           复制文件审核设置(隐含 /O)。
  /Y           取消提示以确认要覆盖现有目标文件。
  /-Y          要提示以确认要覆盖现有目标文件。
  /Z           在可重新启动模式下复制网络文件。
  /B           复制符号链接本身与链接目标相对。
  /J           复制时不使用缓冲的 I/O。推荐复制大文件时使用。

开关 /Y 可以预先在 COPYCMD 环境变量中设置。
这可能被命令行上的 /-Y 覆盖。

```

# 【86/86】WMIC
```


[global switches] <command>



The following global switches are available:

/NAMESPACE           Path for the namespace the alias operate against.

/ROLE                Path for the role containing the alias definitions.

/NODE                Servers the alias will operate against.

/IMPLEVEL            Client impersonation level.

/AUTHLEVEL           Client authentication level.

/LOCALE              Language id the client should use.

/PRIVILEGES          Enable or disable all privileges.

/TRACE               Outputs debugging information to stderr.

/RECORD              Logs all input commands and output.

/INTERACTIVE         Sets or resets the interactive mode.

/FAILFAST            Sets or resets the FailFast mode.

/USER                User to be used during the session.

/PASSWORD            Password to be used for session login.

/OUTPUT              Specifies the mode for output redirection.

/APPEND              Specifies the mode for output redirection.

/AGGREGATE           Sets or resets aggregate mode.

/AUTHORITY           Specifies the <authority type> for the connection.

/?[:<BRIEF|FULL>]    Usage information.



For more information on a specific global switch, type: switch-name /?





The following alias/es are available in the current role:

ALIAS                    - Access to the aliases available on the local system

BASEBOARD                - Base board (also known as a motherboard or system board) management.

BIOS                     - Basic input/output services (BIOS) management.

BOOTCONFIG               - Boot configuration management.

CDROM                    - CD-ROM management.

COMPUTERSYSTEM           - Computer system management.

CPU                      - CPU management.

CSPRODUCT                - Computer system product information from SMBIOS. 

DATAFILE                 - DataFile Management.  

DCOMAPP                  - DCOM Application management.

DESKTOP                  - User's Desktop management.

DESKTOPMONITOR           - Desktop Monitor management.

DEVICEMEMORYADDRESS      - Device memory addresses management.

DISKDRIVE                - Physical disk drive management. 

DISKQUOTA                - Disk space usage for NTFS volumes.

DMACHANNEL               - Direct memory access (DMA) channel management.

ENVIRONMENT              - System environment settings management.

FSDIR                    - Filesystem directory entry management. 

GROUP                    - Group account management. 

IDECONTROLLER            - IDE Controller management.  

IRQ                      - Interrupt request line (IRQ) management. 

JOB                      - Provides  access to the jobs scheduled using the schedule service. 

LOADORDER                - Management of system services that define execution dependencies. 

LOGICALDISK              - Local storage device management.

LOGON                    - LOGON Sessions.  

MEMCACHE                 - Cache memory management.

MEMORYCHIP               - Memory chip information.

MEMPHYSICAL              - Computer system's physical memory management. 

NETCLIENT                - Network Client management.

NETLOGIN                 - Network login information (of a particular user) management. 

NETPROTOCOL              - Protocols (and their network characteristics) management.

NETUSE                   - Active network connection management.

NIC                      - Network Interface Controller (NIC) management.

NICCONFIG                - Network adapter management. 

NTDOMAIN                 - NT Domain management.  

NTEVENT                  - Entries in the NT Event Log.  

NTEVENTLOG               - NT eventlog file management. 

ONBOARDDEVICE            - Management of common adapter devices built into the motherboard (system board).

OS                       - Installed Operating System/s management. 

PAGEFILE                 - Virtual memory file swapping management. 

PAGEFILESET              - Page file settings management. 

PARTITION                - Management of partitioned areas of a physical disk.

PORT                     - I/O port management.

PORTCONNECTOR            - Physical connection ports management.

PRINTER                  - Printer device management. 

PRINTERCONFIG            - Printer device configuration management.  

PRINTJOB                 - Print job management. 

PROCESS                  - Process management. 

PRODUCT                  - Installation package task management. 

QFE                      - Quick Fix Engineering.  

QUOTASETTING             - Setting information for disk quotas on a volume. 

RDACCOUNT                - Remote Desktop connection permission management.

RDNIC                    - Remote Desktop connection management on a specific network adapter.

RDPERMISSIONS            - Permissions to a specific Remote Desktop connection.

RDTOGGLE                 - Turning Remote Desktop listener on or off remotely.

RECOVEROS                - Information that will be gathered from memory when the operating system fails. 

REGISTRY                 - Computer system registry management.

SCSICONTROLLER           - SCSI Controller management.  

SERVER                   - Server information management. 

SERVICE                  - Service application management. 

SHADOWCOPY               - Shadow copy management.

SHADOWSTORAGE            - Shadow copy storage area management.

SHARE                    - Shared resource management. 

SOFTWAREELEMENT          - Management of the  elements of a software product installed on a system.

SOFTWAREFEATURE          - Management of software product subsets of SoftwareElement. 

SOUNDDEV                 - Sound Device management.

STARTUP                  - Management of commands that run automatically when users log onto the computer system.

SYSACCOUNT               - System account management.  

SYSDRIVER                - Management of the system driver for a base service.

SYSTEMENCLOSURE          - Physical system enclosure management.

SYSTEMSLOT               - Management of physical connection points including ports,  slots and peripherals, and proprietary connections points.

TAPEDRIVE                - Tape drive management.  

TEMPERATURE              - Data management of a temperature sensor (electronic thermometer).

TIMEZONE                 - Time zone data management. 

UPS                      - Uninterruptible power supply (UPS) management. 

USERACCOUNT              - User account management.

VOLTAGE                  - Voltage sensor (electronic voltmeter) data management.

VOLUME                   - Local storage volume management.

VOLUMEQUOTASETTING       - Associates the disk quota setting with a specific disk volume. 

VOLUMEUSERQUOTA          - Per user storage volume quota management.

WMISET                   - WMI service operational parameters management. 



For more information on a specific alias, type: alias /?



CLASS     - Escapes to full WMI schema.

PATH      - Escapes to full WMI object paths.

CONTEXT   - Displays the state of all the global switches.

QUIT/EXIT - Exits the program.



For more information on CLASS/PATH/CONTEXT, type: (CLASS | PATH | CONTEXT) /?




```