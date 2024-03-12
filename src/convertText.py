def split_text_by_width(text, width, font):
    lines = []
    current_line = ""
    for word in text.split():
        test_line = current_line + word + " "
        if font.measure(test_line) <= width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return "\n".join(lines)