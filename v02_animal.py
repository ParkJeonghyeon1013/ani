import pathlib

class FileIO:
    def __init__(self, s_path: str) -> None:
        self.__s_path = pathlib.Path(s_path)

    @property
    def s_path(self) -> pathlib.Path:
        return self.__s_path

    @s_path.setter
    def s_path(self, s_path: pathlib.Path) -> None:
        assert isinstance(s_path, pathlib.Path)
        self.__s_path = s_path

    @staticmethod
    def get_anim_name() -> str:
        a_name = input('찾을 동물 이름 적어줘: ')
        return a_name

    @staticmethod
    def get_anim_sound() -> str:
        a_sound = input("동물이 내는 소리를 적어줘: ")
        return a_sound

    def save_to_animal_txt(self, data: str) -> None:
        with open(self.__s_path / 'animal.txt', 'w') as file:
            file.write(data)
            print("저장되었어. 바이.")

    def handler(self):
        self_anim_name = self.get_anim_name()
        self_anim_sound = self.get_anim_sound()

        user_input = input(f"'{self_anim_name}'를(을) animal.txt에 저장할까?? (y/n): ")

        if user_input.lower() == 'n':
            custom_path = self.get_custom_path()
            self.save_to_animal_txt(f'{self_anim_name} / {self_anim_sound}')
        elif user_input.lower() == 'y':
            data = f'{self_anim_name} / {self_anim_sound}'
            if not (self.__s_path / 'animal.txt').exists():
                self.save_to_animal_txt(data)
            else:
                with open(self.__s_path / 'animal.txt', 'a') as file:
                    file.write(f'\n{data}')
                    print(f"'{self_anim_name}'을(를) animal.txt에 추가했어! 바이.")

if __name__ == '__main__':
    fio = FileIO('/Users/ijiyeong/Downloads/')  # animal.txt가 있는 디렉토리 경로를 FileIO()에 넣어줍니다.
    fio.handler()
