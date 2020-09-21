### HTTPRUNNER框架介绍
```大疆
集接口/性能测试于一体的测试框架，可集成jenkins完成自动化测试！
测试用例格式规范：支持json/yaml；可见其中有PyYaml模块的支持；
httprunner2.x主要是对unittest测试框架予以封装重构组织测试用例，
升级之后的httprunner3.x版本更是支持pytest测试框架且集成allure！
```

### hrun支持命令行CLI运行脚本
```
httprunner/hrun -h

可见CLI支持的参数，见名知意：该框架支持哪些功能：

--startproject STARTPROJECT ：用于快速创建一个工程，默认生成api\testcases\testsuites目录

--dot-env-path DOT_ENV_PATH  ：支持指定运行环境配置文件，默认是.env，支持多环境：例如：prod.env\test.env\uat.env

--report-dir REPORT_DIR	: 支持指定生成报告路径，默认当前执行脚本目录下生成reports报告路径

--report-template REPORT_TEMPLATE ：支持指定生成报告模版，该框架支持jinja2模版，默认报告：report_template

 --report-file REPORT_FILE ： 指定生成报告文件名，默认时间错为报告名
 
 --validate	: 校验json格式
 --prettify	：美化json格式
```

### 初始化工程目录介绍
```
hrun -h 查看帮助命令
hrun --startproject httprunner2.x
初始化工程后：
- api		 # 测试用例
- reports    # 测试报告
- templates  # html报告模板
- testcases  # 用例步骤
- testsuites # 测试套件
- debugtalk.py # 热处理文件，可以自定函数在脚本中${func_name}引用
- .env  # 存放了用户数据，如账户密码/请求地址等公共参数
- utils 工具包
```

### 工程使用到httprunner框架的相关技术
##### charles/Fiddler录制脚本使用har2case命令生成json/yaml测试用例文件
- 完整的用例结构(yaml&json)
- 测试用例分层
- 测试用例集
- 重复运行测试用例：testcase中插入times，与name同级
- 跳过用例skip/skipIf/skipUnless
##### 参数化与数据驱动
- extract提取content返回对象
- extract提取参数做上下文接口数据关联
- variables变量声明与引用
- 辅助函数debugtalk.py
- hook机制
- - setup_hooks
- - teardown_hooks
- 环境变量.env
- 外部如何引用csv数据
##### 测试报告ExtentReport
##### locust性能测试


### Jinja2生成报告介绍
- httprunner1.x中有一个extent_report_template，类同allure漂亮的测试报告
- httprunner2.x默认会使用report_template.html模版的测试报告
- httprunner3.x已经支持allure测试报告的输出了，不过需要有allure-pytest/pytest-html插件
```python
- - extent拿1.x版本的扩展目录在2.x应用，选择2.4.3的版本；需要修改源码：

def gen_html_report(summary, report_template=None, report_dir=None, report_file=None):
    """ render html report with specified report name and template

    Args:
        summary (dict): test result summary data
        report_template (str): specify html report template path, template should be in Jinja2 format.
        report_dir (str): specify html report save directory
        report_file (str): specify html report file path, this has higher priority than specifying report dir.

    """
    # 原来使用的是report_template.html报告模版
    if not report_template:
        report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "static",
            "extent_report_template.html"
        )
        logger.log_debug("No html report template specified, use extent_report_template.")
    # 下面使用另一个html报告模版，试试生成啥样，是否只有fail的报告：测试未实现!!!
    elif report_template=="onlyFail":
        report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "static",
            "report_fail_only.html"
        )
        logger.log_debug("No html report template specified, use report_fail_only.")
    # 此处是源码，上面的是替换，hrun 默认生成extent报告，若 report_template 带上default则生成原报告样式
    elif report_template=="default":
        report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "static",
            "report_template.html"
        )
        logger.log_debug("No html report template specified, use default_report_template.")
        
    else:
        logger.log_info("render with html report template: {}".format(report_template))

    logger.log_info("Start to render Html report ...")

    start_at_timestamp = int(summary["time"]["start_at"])
    summary["time"]["start_datetime"] = datetime.fromtimestamp(start_at_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    if report_file:
        report_dir = os.path.dirname(report_file)
        report_file_name = os.path.basename(report_file)
    else:
        report_dir = report_dir or os.path.join(os.getcwd(), "reports")
        report_file_name = "{}.html".format(start_at_timestamp)

    if not os.path.isdir(report_dir):
        os.makedirs(report_dir)

    report_path = os.path.join(report_dir, report_file_name)
    # jinja2使用Template类读取模版类容，讲对应的key传递给template中的变量，输出到report_path
    with io.open(report_template, "r", encoding='utf-8') as fp_r:
        template_content = fp_r.read()
        with io.open(report_path, 'w', encoding='utf-8') as fp_w:
            rendered_content = Template(
                template_content,
                extensions=["jinja2.ext.loopcontrols"]
            ).render(summary)
            fp_w.write(rendered_content)

    logger.log_info("Generated Html report: {}".format(report_path))

    return report_path
```