#!/usr/bin/python
#encoding=utf-8
from __future__ import annotations
import os
import re
import pathlib

'''
[사용 설명]
1. user input 받기
[찾을 경로] [동물 이름] [동물 소리]
2. 동일 이름의 .txt 파일이 있는지 확인
3. 없을 경우, 저장할지 말지 묻기
    있을 경우, 내용 확인 후 변경할지 말지 선택
        변경 안할 경우, 삭제 여부 확인 

'''

class SearchAndSave:
    def __init__(self, s_path: pathlib.Path, s_animal_name: str, s_animal_sound: str) -> None:
        self.__s_path = pathlib.Path(s_path)
        self.__s_animal_name = s_animal_name
        self.__s_animal_sound = s_animal_sound

    def __del__(self) -> None:
        print('SearchAndSave 객체가 메모리에서 제거 되었습니다.')
        pass

    # get_home_path 
    # : 홈디렉토리 경로 반환
    @staticmethod
    def get_home_path() -> pathlib.Path:
        return pathlib.Path.home()


    # 입력받은 디렉토리 경로 반환
    @property
    def s_path(self) -> pathlib.Path:
        return self.__s_path

    # animList 경로 반환
    @property
    def animList_path(self) -> pathlib.Path :
        animList_path = pathlib.Path(f'{self.__s_path}/animList.txt')
        return animList_path

    # animList 존재 반환
    def animList_exist(self) -> bool:
        if self.animList_path.exists():
            print('animList.txt 파일이 존재합니다.') 
            return True
        print('animList.txt 파일이 존재하지 않습니다.') 
        return False

    # animList.txt 제외한 디렉토리에 있는 파일명 리스트로 받기
    def get_files_Path(self) -> list:
        dir_name_list = list()
        for i in self.__s_path.glob('**/*.txt'):
            i = i.as_posix()
            temp = i.replace(self.__s_path.as_posix(), '')
            # file_animName = file_animName.lstrip('/').rstrip('.txt')
            temp = temp.lstrip('/')
            file_anim_name, exr = os.path.splitext(temp)
            dir_name_list.append(file_anim_name)
        return dir_name_list

    # 디렉토리에 있는 파일명 / 소리 형태의 리스트 받기
    def get_dir_fileList(self) -> list[str]:
        file_list = list()
        file_name_list = self.get_files_Path()
        path_list = list(self.__s_path.glob('**/*.txt'))

        for num in range(len(path_list)):
            file_name_list[num] 
            if file_name_list[num] == 'animList':
                continue
            with open(path_list[num].as_posix(), 'r', encoding='UTF8') as f:
                sound = f.readline()
            file_list.append([file_name_list[num], sound])
        return file_list

    # animList.txt에 디렉토리에 있는 파일명과 내용을 넣기
    def write_fileName_to_animList(self) -> None:
        dir_list = self.get_dir_fileList()
        with open(self.animList_path.as_posix(), 'w', encoding='UTF8') as f:
            for i in range(len(dir_list)):
                f.write(f'{dir_list[i][0]} / {dir_list[i][1]}\n')

    # 사용자에게 입력 받은 동물 이름, 소리 세팅
    @property
    def user_input(self) -> list[str]:
        user_anim_list = [self.__s_animal_name, self.__s_animal_sound]
        return user_anim_list

    # animList.txt 파일의 내용을 리스트로 가져오기
    def get_animList(self) -> list:
        with open(self.animList_path.as_posix(), 'r', encoding='UTF8') as f:
            anim_list = f.readlines()
        return anim_list
    
    # animList.txt 의 내용을 이름, 소리로 분류한 리스트 만들기
    def set_animList(self) -> list:
        tmp_lst = list()
        for rl in self.get_animList():
            tmp_anim = rl.rstrip('\n').split(' / ')
            tmp_lst.append(tmp_anim)
        self.anim_list = tmp_lst
        return self.anim_list
    
    
    # animList.txt 에 사용자가 쓴 동물 이름, 소리 추가
    def add_animList(self) -> list:
        with open(self.animList_path.as_posix(), 'a', encoding='UTF8') as f:
            f.write(f'{self.__s_animal_name} / {self.__s_animal_sound}')


    # TODO: 파일 이름과 내용이 동일할 경우로 변경! 현재는 제목만 확인 가능.
    # animList.txt 안에 동물 이름이 존재하는지 확인
    def check_animList(self) -> bool:
        anim_list = self.set_animList()
        for i in range(len(anim_list)):
            if anim_list[i][0] == self.__s_animal_name:
                print(f'\n해당 디렉토리에 {self.__s_animal_name}.txt 이름의 파일이 존재합니다')
                return True

        print(f'\n해당 디렉토리에 {self.__s_animal_name}.txt 이름의 파일이 존재하지 않습니다.')
        return False

    # animList 내용 출력
    def show_directory_content(self):
        print('---------------------------------------------------------------------')
        for animList in self.set_animList():
            print('|',f'[{animList[0]}.txt] 파일에 [{animList[1]}] 이 저장되어있습니다.'.center(50),'|')
        print('---------------------------------------------------------------------\n')

    # 파일이 존재해 해당 파일 안의 내용을 바꿀지 묻는다
    def ask_file_content(self) -> bool:
        change_YN = input(f'\n{self.__s_animal_name}.txt의 내용을 [{self.__s_animal_sound}]로바꿀까요? -- Y/N\n')
        if change_YN.lower() == 'y':
            print(f'\n[{self.__s_animal_name}.txt] 파일의 내용을 [{self.__s_animal_sound}](으)로 새로 저장합니다.')
            return True
        else: 
            print(f'\n[{self.__s_animal_name}.txt] 파일의 내용을 새로 저장하지 않습니다.')
            return False
        
    # 파일 삭제 여부 묻는다
    def ask_delete_file(self) -> bool:
        delete_YN = input(f'\n[{self.__s_animal_name}.txt] 파일을 삭제할까요? -- Y/N\n')
        if delete_YN.lower() == 'y':
            print(f'\n[{self.__s_animal_name}.txt] 파일을 삭제합니다.')
            return True
        else: 
            print(f'\n[{self.__s_animal_name}.txt] 파일을 유지합니다.')
            return False

    # 파일 삭제
    def delete_file(self, delete_YN: bool)-> None:
        file_path = pathlib.Path(f'{self.s_path.as_posix()}/{self.__s_animal_name}.txt')
        if delete_YN == True:
            file_path.unlink()

    # 동물이름 파일에 동물 소리 내용 저장 및 내용 변경
    def save_file(self) -> None:
        with open(f'{self.__s_path.as_posix()}/{self.__s_animal_name}.txt', 'w', encoding='UTF8') as f:
            f.write(self.__s_animal_sound)

    # TODO: handler
    def handler(self) -> int:
        self.write_fileName_to_animList()
        self.show_directory_content()
        check_exist = self.check_animList()

        # 사용자가 입력한 [동물이름.txt]가 존재하면 해당 파일의 내용 바꿀지 말지 묻기
        if check_exist is True:
            change_content = self.ask_file_content()

            # 사용자가 이미 존재하는 [동물이름.txt]의 내용을 바꾸기 원한다면, 
            # 내용 변경 후 animList.txt에 업데이트
            if change_content == True:
                self.save_file()
                self.write_fileName_to_animList()
                self.show_directory_content()

            # 내용 변경 원치 않을 경우 삭제 여부 물음.
            else:
                self.delete_file(self.ask_delete_file())
                self.write_fileName_to_animList()
                self.show_directory_content()

        # 사용자가 입력한 [동물이름.txt]가 존재하지 않으면 파일 생성
        else: 
            print(f'\n[{self.__s_animal_name}.txt] 파일을 새로 생성합니다.')
            self.save_file()
            self.write_fileName_to_animList()
            self.show_directory_content()

        return 0
        


def main():
    user_lst = input('[찾을 경로] [동물 이름] [동물 소리] 순으로 입력해주세요 :\n').split(' ')
    animal_io = SearchAndSave(user_lst[0],user_lst[1], ' '.join(user_lst[2:]))
    animal_io.handler()
  
if __name__ == '__main__':
    print('\n>>>>>>>>>>>>>>> save_search_animal.py <<<<<<<<<<<<< ')
    print('각 요소는 띄어쓰기로 구분합니다!\nex)/rapa/home/ 고양이 야옹\n')
    # sample ---> c:/Users/USER/Desktop/ani/ 사자 어흥
    # fio = SearchAndSave('c:/Users/USER/Desktop/ani/', '사자', '어흥')
    # fio.show_directory_content()
    
    main()
