from fatsecret import BaseFatsecretError


# чтобы из-за ошибки от FS все не падало
def fs_error_catcher(method):
    def wrapper(self, *args, **kwargs):

        try:
            return method(self, *args, **kwargs)
        except BaseFatsecretError as error:
            print("Возникла ошибка связанная с FS!")
            print(error)

    return wrapper