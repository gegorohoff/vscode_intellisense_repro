I have looked and do not see any tickets specifically addressing this issue, nor with explicit repro instructions to triage. My apologies if my search failed to find existing relevant tickets, but hopefully my repro instructions can help regardless.

## Environment data

-   VS Code version: **1.55.2 and 1.56.0-insider**
-   Extension version (available under the Extensions sidebar): **2021.4.765268190**
-   OS and version: **Win 10 20H2 (19042.928) x64 10.0.19042. WSL 2 using Ubuntu 20.04 (4.19.128-microsoft-standard)**
-   Python version: **3.9.4 (Anaconda 4.10.1)**
-   Type of virtual environment used : **anaconda**
-   Relevant/affected Python packages and their versions: **all?**
-   Relevant/affected Python-related VS Code extensions and their versions: no other extensions, disabled _everything_ for repro.
-   Value of the `python.languageServer` setting: **jedi | jediLSP**

[**NOTE**: If you suspect that your issue is related to the Microsoft Python Language Server (`python.languageServer: 'Microsoft'`), please download our new language server [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) from the VS Code marketplace to see if that fixes your issue]

I wrote all the repro before starting this report. Pylance seems to work fine! HOWEVER, it is not the default language server. As such, I feel this is still valuable, although it may be a Jedi issue. I am happy to file this with them if that is the more appropriate place for this issue.

## Expected behaviour

I am developing part of a shared package hierarchy. That is, my module 'labtech.utils.api' needs to reference elements of 'labtech.utils.log' which is not in the workspace, and is pip-installed from a separate repo/workspace. I expect typing

`from labtech.utils.`

would allow me to auto-complete and reference definitions of the 'log' package within there.


## Actual behaviour

Working on a file in the 'api' package should be able to use Intellisense on symbols in the 'log' package that is pip-installed. Instead, because the 'labtech.utils' dir within the 'api' workspace lacks the 'log' code, intellisense sees nothing and only gives me elements from the current workspace - those under 'api' - which completely cripples intellisense. It is vice-versa for working on a file in 'log' and trying to reference 'api' or anything else besides 'log'

Everything works normally if the workspace doesn't contain the 'labtech' directory. (e.g. for something completely different)

## Steps to reproduce:

Files and structure are in this repo for superb convenience: https://github.com/gegorohoff/vscode_intellisense_repro


    WSL2 Bash:
        conda create --name goto_def python
        conda activate goto_def
        cd ~
        git clone git@github.com:gegorohoff/vscode_intellisense_repro.git goto_def
        cd goto_def
        # populate with contents. Should have ~/goto_def/pkg_A and ~/goto_def/pkg_B

        # The helper files don't YET work because the libraries aren't installed with pip:
        python pkg_A/labtech/utils/log/helper.py
        #   ModuleNotFoundError: No module named 'labtech.utils.log'
        python pkg_B/labtech/utils/api/helper.py
        #   ModuleNotFoundError: No module named 'labtech.utils.api'

        pip install ./pkg_A
        pip install ./pkg_B
        # You will see that ~/anaconda3/envs/goto_def/lib/python3.9/site-packages has labtech/utils/api and labtech/utils/log and associated libs underneath

        # The helper files now work:
        python pkg_A/labtech/utils/log/helper.py
        #   the logs are empty
        python pkg_B/labtech/utils/api/helper.py
        #   login failed
        python pkg_A/labtech/utils/log/runner.py # this imports labtech.utils.api.helper:Helper
        #   login failed

        # Now we open code to demonstrate the issue with intellisense
        code pkg_A

    In Code, using workspace as directory pkg_A (not the root of this repro repo!):
        Set the Python interpreter to the goto_def conda env.

        Open the file labtech/utils/log/Runner.py
        Try intellisense on this 'Helper' or any part of this line.
            from labtech.utils.api.helper import Helper
        Try to re-write the import; note how you can only reference labtech.utils.log and nothing in labtech.utils.api which clearly works based on the output of the previous step.


## Logs

https://github.com/gegorohoff/vscode_intellisense_repro/blob/main/vscode_python_log.txt
