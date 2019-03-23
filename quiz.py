from cryptography.fernet import Fernet


def quiz():
    key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

    # Oh no! The code is going over the edge! What are you going to do?
    message = b'gAAAAABckecguWXCkDKk8YyufVMjZs3QjZXTyOV4Fm7xjR2Y75jRZQSSnVPg76U0kprye9qLbFCpTohYi6a60BK9Lb' \
              b'v6vSYEQ4CaTZYepmcOy2_VbbczJm6GUuOg6JGwu2uIqLVfPPe3l11ToO59DEG14aeM03aot326lpbmqi9CvhfiC7is' \
              b'O09miUB9YXOBxEJE2zkUBY1G'

    f = Fernet(key)
    r = f.decrypt(message)
    print(r)


if __name__ != "__main__":
    quiz()
