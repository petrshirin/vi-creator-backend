import os
import uuid


class FileUploadTo(object):
    """
    Класс, который заменяет множество функций upload_to
    filename: uuid4 строка
    exp: расширение исходного файла
    USAGE:
        FileUploadTo('emotions') - сохранит файл так: media/emotions/filename.exp

        FileUploadTo('emotions', parent_instance='user') - сохранит файл так: media/emotions/{user.pk}/filename.exp
    """

    def __init__(self, path, *args, **kwargs):
        """

        :param path: str - путь до папки, куда сохранять файлы
        :param args:
        :param kwargs:
            parent_instance: str - дополнительная папка для сохранения, нужно для того,
            чтобы можно было разделять файлы в основной папке по категориям. Например по пользователям
        """
        self.parent_instance = kwargs.get('parent_instance', None)
        if self.parent_instance:
            self.path = os.path.join(path, "%s%s%s")
        else:
            self.path = os.path.join(path, "%s%s")

    def get_file_path(self, instance, filename):
        exp = os.path.splitext(filename)[1]
        if self.parent_instance and hasattr(instance, self.parent_instance):
            parent_instance = getattr(instance, self.parent_instance)
            return self.path % (parent_instance.pk, uuid.uuid4(), exp)
        return self.path % (uuid.uuid4(), exp)
