# PbxBot v3 Plugins

# Follow this format to make your own plugin for PbxBot.

```python3
"""
A sample code to display hello without taking input.
"""
# this is a mandatory import
from . import on_message, Pbxbot, HelpMenu

# assigning command
@on_message("hii")
async def hi(_, message):
    # command body
    await Pbxbot.edit(message, "Hello!")


# to display in help menu
HelpMenu("hii").add(
  "hii", None, "Says Hello!"
).done()
```

```python3
"""
A sample code to display hello with input.
"""
# this is a mandatory import
from . import on_message, Pbxbot, HelpMenu

# assigning command
@on_message("hii", allow_stan=True)
async def hi(_, message):
    # command body
    msg = await Pbxbot.input(message)
    if msg:
        await Pbxbot.edit(message, f"Hello! {msg}")
    else:
        await Pbxbot.edit(message, "Hello!")


# to display in help menu
HelpMenu("hii").add(
    "hii", "<text>", "Display Hello with a input!"
).done()
```


## To get more functions read codes in repo.
