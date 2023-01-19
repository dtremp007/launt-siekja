#!/bin/zsh
zsh_config=$HOME/.zshrc
python_script=launt-siekja/siekjen.py
new_path="export PATH=\"$(pwd)/launt-siekja:\$PATH\""

if command -v python3 &> /dev/null;
then
    python_command=$(command -v python3)
elif command -v python &> /dev/null;
then
    python_command=$(command -v python)
else
    echo "Can't find python." && exit 1
fi

# Add path to .zshrc
if [[ -w $zsh_config ]];
then
    if ! grep -F "# launt-siekja" $zsh_config;
    then
    {
        echo -e "# launt-siekja"
        echo "$new_path"
    } >> "$zsh_config"
    fi
else
    echo "You will need to manually add path."
fi

# Replace shebang if it's not the right one
if [[ "$(head -n 1 $python_script)" != "#!${python_command}" ]];
then
    rest_of_file=$(tail -n +2 "$python_script")
    echo "#!${python_command}" > "$python_script"
    echo "$rest_of_file" >> "$python_script"
fi

# Check if the requirements.txt file exists
if [[ -f "requirements.txt" ]]; then
    # Install the required packages
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    else
        echo "Could not find pip" && exit 1
    fi
fi

chmod +x "$python_script" || echo "Failed to set permission on python script"
