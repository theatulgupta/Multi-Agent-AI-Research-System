# Streamlit Cloud Deployment Fix

## Problems Fixed

### 1. lxml Build Error (SOLVED ✅)
**Error**: `/usr/bin/ld: cannot find -lz: No such file or directory`

**Root Cause**:
- Python 3.14 incompatibility with lxml 5.3.0
- Missing zlib development package
- lxml trying to build from source

**Solution**:
- Created `runtime.txt` with `python-3.11`
- Added `zlib1g-dev` to `packages.txt`
- Downgraded lxml to 5.2.2

### 2. ImportError (SOLVED ✅)
**Error**: `cannot import name 'create_agent' from 'langchain.agents'`

**Root Cause**:
- `create_agent` was deprecated and removed from `langchain.agents`
- Moved to `langgraph.prebuilt` in newer versions

**Solution**:
- Changed import from `langchain.agents.create_agent`
- To `langgraph.prebuilt.create_react_agent`
- Updated function calls: `create_agent(model=llm, tools=[...])` → `create_react_agent(llm, [...])`

## Solutions Applied

### Fix 1: Python Version & Dependencies

**Created `runtime.txt`**:
```
python-3.11
```

**Updated `packages.txt`**:
```
libxml2-dev
libxslt1-dev
zlib1g-dev  # ADDED THIS
```

**Updated `requirements.txt`**:
```
lxml==5.2.2  # Changed from 5.3.0
```

### Fix 2: Import Error

**Updated `agents.py`**:
```python
# OLD (deprecated)
from langchain.agents import create_agent
return create_agent(model=llm, tools=[web_search])

# NEW (correct)
from langgraph.prebuilt import create_react_agent
return create_react_agent(llm, [web_search])
```

## Why This Works

**Python 3.11**:
- More stable for AI/ML libraries
- Better wheel availability
- Tested by most package maintainers

**zlib1g-dev**:
- Provides the `libz.so` shared library
- Required by lxml for compression support
- Fixes the linker error

**lxml 5.2.2**:
- Has prebuilt wheels for Python 3.11
- More stable than 5.3.0
- Avoids source compilation

**create_react_agent**:
- Modern replacement for deprecated create_agent
- Part of langgraph.prebuilt module
- Better integration with latest LangChain ecosystem

## Commits

1. **Fix lxml and Python version** (86d71c7):
   ```
   fix: resolve Streamlit Cloud deployment issues
   - Add runtime.txt to specify Python 3.11
   - Add zlib1g-dev to packages.txt
   - Downgrade lxml from 5.3.0 to 5.2.2
   ```

2. **Fix import error** (bd65751):
   ```
   fix: use create_react_agent from langgraph.prebuilt
   - Replace deprecated create_agent
   - Fixes ImportError on Streamlit Cloud
   ```
