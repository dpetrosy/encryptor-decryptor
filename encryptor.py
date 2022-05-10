import sys

# Driver code
def main():
    # user choose mode
    print("Print \"encrypt\" if you want to encrypt your text.")
    print("Print \"decrypt\" if you want to decrypt your text.")
    encrypt_or_decrypt = input(">> ")
    if not ((encrypt_or_decrypt == "encrypt") or (encrypt_or_decrypt == "decrypt")):
        sys.exit("\nYour inputed mode have wrong format, try again and be attentive!")
        
    # get keys and make them usable
    key1 = (input("\nInput first key: ")).lower()
    key2 = (input("Input second key: ")).lower()
    
    key1 = key1.replace("j", "i")
    key2 = key2.replace("j", "i")
    
    key1 = clean_key(key1);
    key2 = clean_key(key2);
    
    key1 = "".join(dict.fromkeys(key1))
    key2 = "".join(dict.fromkeys(key2))
    
    # make matrix
    columns = rows = 11;
    matrix = [([0] * columns) for i in range(rows)]
    make_matrix(matrix, key1, key2, rows, columns)
    
    # get user input and chosen mode
    user_input = get_user_input()
    user_text = user_input[0]
    choosed_mode = user_input[1]
    
    user_text = user_text.replace("j", "i")
    user_text = user_text.replace("J", "I")
    
    # get final text sending corresponding function as argument
    if encrypt_or_decrypt == "encrypt":
        final_text = get_final_text(user_text, matrix, get_encrypted_letters)
    else:
        final_text = get_final_text(user_text, matrix, get_decrypted_letters)
        
    # if chosen mode is "console", print result in console, else write in file "output.txt"
    final_text = f"key1 = {key1}\nkey2 = {key2}\n" + get_str_matrix(matrix, rows, columns) + "\n" + "Your text: \n\n" + final_text
    if choosed_mode == "console":
        print(final_text)
    else:
        try:
            output_file = open("output.txt", "w")
        except BaseException:
            sys.exit(f"\nCan not open file \"output.txt\", try again!")
        output_file.write(final_text)
        output_file.close()
        print(f"\nYour {encrypt_or_decrypt}ed text written in file \"output.txt\"!")
        

# clear key from non-alphabetic characters
def clean_key(key):
    for i in key:
        if not i.isalpha():
            key = key.replace(i, "")
    return key
    

# make matrix using key1 and key2
def make_matrix(matrix, key1, key2, rows, columns):
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    right_square = get_squares(key1)
    left_square = get_squares(key2)
    
    a = r = l = 0
    for i in range(1, rows):
        if a == 25:
            a = 0
        for j in range(1, columns):
            if (i <= 5 and j <= 5) or (i >= 6 and j >= 6):
                matrix[i][j] = alphabet[a]
                a += 1
            elif i <= 6 and j >= 6:
                matrix[i][j] = right_square[r]
                r += 1
            else:
                matrix[i][j] = left_square[l]
                l += 1


# make and return squares made with keys
def get_squares(key):
    square = "abcdefghiklmnopqrstuvwxyz"
    
    for i in key:
        square = square.replace(i, "")
        
    square = key + square
    return square


# get and return user input 
def get_user_input():
    # user choose input mode
    choosed_mode = input("\nIf you want input your text in console print \"console\".\nIf you want print file name, print \"file\".\n>> ")
    if not ((choosed_mode == "console") or (choosed_mode == "file")):
        sys.exit("\nYour inputed mode have wrong format, try again and be attentive!")
        
    # if chosen mode is "console", get input from console, else get from user file
    if choosed_mode == "console":
        user_input = input("\nInput your text: ")
    else:
        file_name = input("\nInput file name: ")
        try:
            input_file = open(file_name, "r")
        except BaseException:
            sys.exit(f"\nCan not open file \"{file_name}\", try again!")
        user_input = input_file.read()
        input_file.close()
        
    return [user_input, choosed_mode]
        

# get final text, depends on the selected mode, "encrypt" or "decrypt"
def get_final_text(user_text, matrix, get_letters):
    subtext = ""
    final_text = ""
    non_alpha_letters = ""
    
    j = 0
    for i in user_text:
        if i.isalpha():
            subtext += i
            j += 1
            if j == 2:
                letters = get_letters(matrix, subtext)
                if not (len(non_alpha_letters) == 0):
                    final_text += (letters[0] + non_alpha_letters + letters[1])
                    non_alpha_letters = ""
                else:
                    final_text += letters
                subtext = ""
                j = 0
        elif (j == 1):
            non_alpha_letters += i
        else:
            final_text += i
    if  not (get_letters_count(user_text) % 2 == 0):
        final_text += subtext
    if not (user_text[-1].isalpha()):
        final_text += non_alpha_letters
    return final_text
        

# get and return pair of encrypted letters
def get_encrypted_letters(matrix, subtext):
    left_square_indexes = find_letter(matrix, subtext[0], 1, 1, 6, 6)
    right_square_indexes = find_letter(matrix, subtext[1], 6, 6, 11, 11)

    left_letter = matrix[right_square_indexes[0]][left_square_indexes[1]]
    right_letter = matrix[left_square_indexes[0]][right_square_indexes[1]]
    
    if (subtext[0].isupper()):
        left_letter = left_letter.upper()
    if (subtext[1].isupper()):
        right_letter = right_letter.upper()
        
    return (left_letter + right_letter)


# get and return pair of decrypted letters
def get_decrypted_letters(matrix, subtext):
    left_square_indexes = find_letter(matrix, subtext[0], 6, 1, 11, 6)
    right_square_indexes = find_letter(matrix, subtext[1], 1, 6, 6, 11)

    left_letter = matrix[right_square_indexes[0]][left_square_indexes[1]]
    right_letter = matrix[left_square_indexes[0]][right_square_indexes[1]]
    
    if (subtext[0].isupper()):
        left_letter = left_letter.upper()
    if (subtext[1].isupper()):
        right_letter = right_letter.upper()
    return (left_letter + right_letter)


# find given letter in given matrix square and return pair of indexes [i, j]
def find_letter(matrix, letter, start_i, start_j, max_i, max_j):
    indexes = []
    
    letter = letter.lower()
    for i in range (start_i, max_i):
        for j in range (start_j, max_j):
            if (matrix[i][j] == letter):
                return [i, j]


# get user input text letters count
def get_letters_count(user_text):
    count = 0
    for i in user_text:
        if (i.isalpha()):
            count += 1
    return count
    

# get matrix, collect it in string and return the resulting string
def get_str_matrix(matrix, rows, columns):
    output_text = ""
    output_text += "\n"
    
    for i in range(1, rows):
        if i == 6:
            for k in range (rows):
                if (k == 5):
                    output_text += "+ "
                    continue
                output_text += "- "
            output_text += "\n"
        for j in range(1, columns):
            if j == 6:
                output_text += "| "
            output_text += matrix[i][j] + " "
        output_text += "\n"
    return output_text


if __name__ == "__main__":
    main()