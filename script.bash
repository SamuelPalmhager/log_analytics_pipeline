if [ $# -gt 0 ]; then
    filename="$1"
else
    echo "No argument passed, defaulting to test.db."
    filename="test"
fi

python3 main.py "$filename"

rm "${filename}.json"