# Streamlit Cloud Deployment Fix

## Problem
App was failing to deploy on Streamlit Cloud with error:
```
/usr/bin/ld: cannot find -lz: No such file or directory
```

## Root Cause
1. **Python 3.14 incompatibility**: lxml 5.3.0 doesn't have prebuilt wheels for Python 3.14
2. **Missing system dependency**: zlib development package (zlib1g-dev) was not installed
3. **Build from source failing**: lxml tried to build from source but couldn't find zlib

## Solution Applied

### 1. Created `runtime.txt`
```
python-3.11
```
Forces Streamlit Cloud to use Python 3.11 instead of 3.14 for better stability.

### 2. Updated `packages.txt`
```
libxml2-dev
libxslt1-dev
zlib1g-dev  # ADDED THIS
```
Added zlib1g-dev to provide the missing `-lz` linker dependency.

### 3. Downgraded lxml in `requirements.txt`
```
lxml==5.2.2  # Changed from 5.3.0
```
Version 5.2.2 has better compatibility with both Python 3.11 and 3.12.

### 4. Updated Documentation
- Added deployment troubleshooting to DEPLOYMENT.md
- Updated README with deployment notes
- Documented the importance of each deployment file

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

## Testing
1. Push to GitHub: ✅
2. Streamlit Cloud will automatically redeploy
3. Check build logs for success
4. Test app functionality

## Expected Result
App should now deploy successfully on Streamlit Cloud without build errors.

## Commit
```
fix: resolve Streamlit Cloud deployment issues
- Add runtime.txt to specify Python 3.11 for stability
- Add zlib1g-dev to packages.txt to fix lxml build error
- Downgrade lxml from 5.3.0 to 5.2.2 for better compatibility
```

Commit hash: 86d71c7
