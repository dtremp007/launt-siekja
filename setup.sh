#!/bin/zsh
zsh_config=$HOME/.zshrc
python_script=launt-siekja/siekjen.py
new_path="export PATH=\"$(pwd)/launt-siekja:\$PATH\""

# Add path to .zshrc
if [[ -w $zsh_config ]]; then
    {
        echo -e "\n# launt-siekja"
        echo "$new_path"
    } >> "$zsh_config"
else
    echo "You will need to manually add path."
fi

# Replace shebang if it's not the right one
if [[ "$(head -n 1 $python_script)" != "#!$(where python)" ]]; then
    rest_of_file=$(tail -n +2 "$python_script")
    echo "#!$(where python)" > "$python_script"
    echo "$rest_of_file" >> "$python_script"
fi

# Check if the requirements.txt file exists
if [[ -f "requirements.txt" ]]; then
    # Install the required packages
    pip install -r requirements.txt
fi

chmod +x "$python_script" ||
    error "Failed to set permission on python script"
