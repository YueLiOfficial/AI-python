try:
    a = int(input("请输入第一个数: "))
    b = int(input("请输入第二个数: "))
    result = a / b
    print(result)
# except (ZeroDivisionError, ValueError)
except ZeroDivisionError:
    print("[程序异常], 0不能作为除数")
except ValueError:
    print("[程序异常],  输入的必须是数字")
except Exception as e:
    print(f"[异常], 异常信息:{e}")
    print(f"[异常], 异常类型{type(e)}")
    print(f"[异常], 异常参数{e.args}")
    print(f"[异常], 异常的文件{e.__traceback__.tb_frame.f_code.co_filename}")
    print(f"[异常], 异常的行数{e.__traceback__.tb_lineno}")

    # 通过traceback来回溯异常
    import traceback
    print(traceback.format_exc())
