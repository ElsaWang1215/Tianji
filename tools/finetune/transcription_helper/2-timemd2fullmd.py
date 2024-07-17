import glob
import os
import re
psth = './audio_md/*'
output_file_directory = "./audio_md_full"
path = glob.glob(psth)
length = len(path)

if not os.path.exists(output_file_directory):
    os.mkdir(output_file_directory)

for i in range(length):
    input_file_path = path[i]
    output_file_name = os.path.basename(input_file_path)
    def extract_clean_text(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # Remove time stamps and < No Speech > markers
        cleaned_text = re.sub(r'\[\d+,\d{2}:\d{2}\]\s*< No Speech >', '', content)
        cleaned_text = re.sub(r'\[\d+,\d{2}:\d{2}\]', '', cleaned_text)
        cleaned_text = re.sub(r'< No Speech >', '', cleaned_text)

        # Remove any additional non-content text
        cleaned_text = re.sub(r'<video.*?>.*?</video>', '', cleaned_text, flags=re.DOTALL)
        cleaned_text = re.sub(r'Texts generated.*?\.srt\)', '', cleaned_text, flags=re.DOTALL)
        
        cleaned_text = re.sub(r'Mark the sentences.*?subtitle context\.', '', cleaned_text, flags=re.DOTALL)
        cleaned_text = re.sub(r'- \[.*?\]\s*', '', cleaned_text)
        cleaned_text = re.sub(r'<-- Mark if you are done editing\.\s*\.', '', cleaned_text)
        # Clean up remaining spaces and newlines
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        # Remove spaces around punctuation
        cleaned_text = re.sub(r'\s([.,!?;:])', r'\1', cleaned_text)
        cleaned_text = re.sub(r'([.,!?;:])\s', r'\1', cleaned_text)

        # Replace remaining spaces with commas where appropriate
        formatted_text = re.sub(r'(\S)\s+(\S)', r'\1,\2', cleaned_text)
        # Ensure no comma follows a period
        formatted_text = re.sub(r'\。,', '。', formatted_text)
            # Remove special characters except for punctuation and alphanumeric
        formatted_text = re.sub(r'[^\w\s.,!?;:]', '', formatted_text)
        return formatted_text
    # Example usage
    extracted_text = extract_clean_text(input_file_path)
    output_file_path = os.path.join(output_file_directory, output_file_name)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(extracted_text)

