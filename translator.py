from google_trans_new import google_translator


# 会报错：json.decoder.JSONDecodeError: Extra data: line 1 column 379 (char 378)
# 解决方法：将代码151行修改为 response = decoded_line
def google_trans(src, tgt, text):
    translate_text = ''
    try:
        translator = google_translator()
        translate_text = translator.translate(text, lang_tgt=tgt, lang_src=src)
    except Exception as e:
        raise e
    finally:
        return translate_text
