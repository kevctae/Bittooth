#!/bin/zsh

# Define functions
err(){
    echo "[Error] $*" >>/dev/stderr
}
suc(){
    echo "[Success] $*" >>/dev/stdout
}
act(){
    echo "[Action] $*" >>/dev/stdout
}

# Check if Homebrew is installed
if brew_version=$(brew --version | head -n 1) ; then
    suc "$brew_version requirement satisfied"
else
    err "Homebrew not installed!"
    exit 65
fi

# Check if pyenv is installed
if pyenv_version=$(pyenv --version) ; then
    suc "$pyenv_version requirement satisfied"
else
    err "pyenv not installed!"
    exit 65
fi

# Check if pyenv-virtualenv is installed
if pyenv_virtualenv_version=$(pyenv virtualenv --version) ; then
    suc "$pyenv_virtualenv_version requirement satisfied"
else
    err "pyenv-virtualenv not installed!"
    exit 65
fi

# Check if Python 3.8.12 is installed
if pyenv versions | grep "3.8.12$" > /dev/null ; then
    suc "Python 3.8.12 requirement satisfied"
else
    err "Python 3.8.12 not installed!"
    act "Installing Python 3.8.12"
    
    pyenv install 3.8.12

    suc "Successfully installed Python 3.8.12"
fi

# Create a virtual environment bittooth
if pyenv versions | grep "bittooth$" > /dev/null; then
    suc "'bittooth' virtual environment requirement satisfied"
else
    err "'bittooth' virtual environment not created!"
    act "Creating 'bittooth' virtual environment"
    
    pyenv virtualenv 3.8.12 bittooth

    suc "Successfully created 'bittooth' virtual environment"
fi

# Move to root project folder
cd ..

# Check current virtual environment
if pyenv version | grep "bittooth " > /dev/null; then
    suc "'bittooth' is the current virtual environment"
else
    err "'bittooth' is NOT the current virtual environment"
    act "Changing virtual environment to 'bittooth"
    
    pyenv local bittooth

    suc "Successfully changed virtual environment to 'bittooth'"
fi

if python --version | grep "3.8.12"; then
    act "Installing dependencies"

    # Upgrade pip
    pip install --upgrade pip

    # Install twint
    pip install -e ./src/twint -r ./src/twint/requirements.txt

    # Install requirements
    pip install -r ./setup/requirements.txt

    # Download model
    spacy download en_core_web_sm

    suc "Setup finished!"
else
    err "Incorrect Python version!"
    err "Setup failed!"
    exit 65
fi

exit 0