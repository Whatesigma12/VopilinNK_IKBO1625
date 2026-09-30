# Практическая работа №1
## Task 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep)

```bash
grep -o '^[^:]*' /etc/passwd | sort
```
выведеные данные:
bin
cron
daemon
dhcpcd
ftp
games
guest
halt
klogd
lp
mail
news
nobody
ntp
root
shutdown
sshd
svn
sync
uucp

## Task 2
Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере

```bash
awk {'print $2, $1'} /etc/protocols | sort -n -r | head -n 5
```
выходные данные:
262 mptcp
143 ethernet
142 rohc
141 wesp
140 shim6

## Task 3
Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!)

терминал:
```bash
nano banner
```
nano:
```bash
#!/bin/bash

text="$1"
len=$((${#text} + 2))
border=$(printf '%*s' "$len" '' | tr ' ' '-')

echo "+${border}+"
echo "| ${text} |"
echo "+${border}+"
```
терминал: 
```bash
./banner "Hello from RTU MIREA!"
```

## Задача 4

Написать программу для вывода всех идентификаторов из файла без повторений.

Создаем файл `identifiers.sh`:

```bash
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Укажите файл"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Файл не найден"
    exit 1
fi

grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u | tr '\n' ' '
echo
```

Даем файлу право на выполнение:

```bash
chmod +x identifiers.sh
```

Для проверки создадим файл `hello.c`:

```c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
    return 0;
}
```

Запуск:

```bash
./identifiers.sh hello.c
```

Результат:

```text
h hello include int main n printf return stdio void world
```

Программа получает имя файла через `$1`.

`grep` ищет в файле слова, которые подходят под правила имен идентификаторов C/C++ и Java.

`sort -u` сортирует найденные слова и удаляет повторения.

`tr` выводит результат в одну строку.

---

## Задача 5

Написать программу для регистрации пользовательской команды.

Создаем файл `reg`:

```bash
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Укажите файл программы"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Файл не найден"
    exit 1
fi

chmod 755 "$1"

sudo cp "$1" /usr/local/bin/

echo "Команда установлена: $(basename "$1")"
```

Даем программе право на выполнение:

```bash
chmod +x reg
```

Например, регистрируем созданную ранее программу `banner`:

```bash
./reg banner
```

Результат:

```text
Команда установлена: banner
```

Проверяем:

```bash
ls -l /usr/local/bin/banner
```

После копирования программу можно запускать уже без `./`:

```bash
banner "Hello MIREA"
```

Результат:

```text
+-------------+
| Hello MIREA |
+-------------+
```

Команда:

```bash
chmod 755
```

задает права на чтение и выполнение программы.

Команда:

```bash
cp
```

копирует программу в `/usr/local/bin`.

Так как `/usr/local/bin` находится в `PATH`, установленную программу можно запускать как обычную команду Linux.

---

## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением `.c`, `.js` и `.py`.

Создаем файл `check_comments.sh`:

```bash
#!/bin/bash

dir="${1:-.}"

if [ ! -d "$dir" ]; then
    echo "Каталог не найден"
    exit 1
fi

find "$dir" -type f \( -name "*.c" -o -name "*.js" -o -name "*.py" \) |
while read -r file
do
    first_line=$(head -n 1 "$file")

    case "$file" in

        *.py)
            if echo "$first_line" | grep -qE '^[[:space:]]*#'; then
                echo "$file - комментарий есть"
            else
                echo "$file - комментария нет"
            fi
            ;;

        *.c|*.js)
            if echo "$first_line" | grep -qE '^[[:space:]]*(//|/\*)'; then
                echo "$file - комментарий есть"
            else
                echo "$file - комментария нет"
            fi
            ;;

    esac
done
```

Даем право на выполнение:

```bash
chmod +x check_comments.sh
```

Для проверки создадим несколько файлов:

```bash
mkdir -p test6

printf '// комментарий\nint main(){}\n' > test6/program.c
printf 'int main(){}\n' > test6/test.c

printf '// комментарий\nlet x = 5;\n' > test6/script.js
printf 'let x = 5;\n' > test6/main.js

printf '# комментарий\nprint("Hello")\n' > test6/program.py
printf 'print("Hello")\n' > test6/test.py
```

Запускаем:

```bash
./check_comments.sh test6
```

Пример результата:

```text
test6/program.c - комментарий есть
test6/test.c - комментария нет
test6/script.js - комментарий есть
test6/main.js - комментария нет
test6/program.py - комментарий есть
test6/test.py - комментария нет
```

`find` ищет файлы с нужными расширениями.

`head -n 1` получает первую строку файла.

После этого программа проверяет, начинается ли первая строка с символов комментария.

Для Python проверяется:

```text
#
```

Для C и JavaScript:

```text
//
// /*
```

---

## Задача 7

Написать программу для поиска файлов-дубликатов в указанном каталоге и его подкаталогах.

Создаем файл `duplicates.sh`:

```bash
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Укажите каталог"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Каталог не найден"
    exit 1
fi

find "$1" -type f -exec sha256sum {} + |
sort |
uniq -w 64 -D
```

Даем право на выполнение:

```bash
chmod +x duplicates.sh
```

Создадим каталог для проверки:

```bash
mkdir -p test7/sub
```

Создаем несколько файлов:

```bash
echo "hello" > test7/file1.txt
echo "hello" > test7/file2.txt
echo "other" > test7/file3.txt
echo "hello" > test7/sub/file4.txt
```

Запускаем:

```bash
./duplicates.sh test7
```

Пример результата:

```text
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03  test7/file1.txt
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03  test7/file2.txt
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03  test7/sub/file4.txt
```

`find` находит все файлы в каталоге и его подкаталогах.

`sha256sum` вычисляет для каждого файла контрольную сумму.

Если содержимое двух файлов одинаковое, их контрольные суммы тоже будут одинаковыми.

`sort` сортирует полученные значения.

`uniq -D` оставляет повторяющиеся контрольные суммы, то есть файлы-дубликаты.

---

## Задача 8

Написать программу, которая находит файлы с указанным расширением и добавляет их в архив `.tar`.

Создаем файл `archive.sh`:

```bash
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Укажите расширение файлов"
    exit 1
fi

ext="${1#.}"
archive="files_${ext}.tar"
list=".archive_list"

find . -maxdepth 1 -type f -name "*.$ext" > "$list"

if [ ! -s "$list" ]; then
    echo "Файлы с расширением .$ext не найдены"
    rm "$list"
    exit 0
fi

tar -cf "$archive" -T "$list"

rm "$list"

echo "Создан архив: $archive"
```

Даем право на выполнение:

```bash
chmod +x archive.sh
```

Для проверки создадим несколько файлов:

```bash
echo "one" > first.txt
echo "two" > second.txt
echo "three" > third.c
```

Запуск для файлов `.txt`:

```bash
./archive.sh txt
```

Результат:

```text
Создан архив: files_txt.tar
```

Проверяем содержимое архива:

```bash
tar -tf files_txt.tar
```

Результат:

```text
./first.txt
./second.txt
```

Переменная:

```bash
ext
```

содержит нужное расширение.

`find` ищет файлы с этим расширением только в текущем каталоге.

`tar -cf` создает архив.

Временный файл `.archive_list` содержит список файлов, которые необходимо добавить в архив.

После создания архива временный список удаляется.

---

## Задача 9

Написать программу, которая заменяет последовательности из четырех пробелов на символ табуляции.

Создаем файл `spaces_to_tabs.sh`:

```bash
#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Укажите входной и выходной файлы"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Входной файл не найден"
    exit 1
fi

sed 's/    /\t/g' "$1" > "$2"

echo "Готово. Результат записан в $2"
```

Даем право на выполнение:

```bash
chmod +x spaces_to_tabs.sh
```

Создадим тестовый файл:

```bash
printf 'int main()\n{\n    return 0;\n}\n' > input.txt
```

Запускаем программу:

```bash
./spaces_to_tabs.sh input.txt output.txt
```

Результат:

```text
Готово. Результат записан в output.txt
```

Проверяем файл:

```bash
cat -A output.txt
```

Пример результата:

```text
int main()$
{$
^Ireturn 0;$
}$
```

Обозначение:

```text
^I
```

показывает символ табуляции.

`sed` ищет четыре пробела подряд и заменяет их на символ табуляции.

`$1` - входной файл.

`$2` - выходной файл.

---

## Задача 10

Написать программу для поиска пустых текстовых файлов в указанной директории.

Создаем файл `empty_files.sh`:

```bash
#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Укажите директорию"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Директория не найдена"
    exit 1
fi

find "$1" -maxdepth 1 -type f -name "*.txt" -empty -printf '%f\n'
```

Даем право на выполнение:

```bash
chmod +x empty_files.sh
```

Создаем каталог для проверки:

```bash
mkdir -p test10
```

Создаем два пустых текстовых файла:

```bash
touch test10/empty1.txt
touch test10/empty2.txt
```

Также создадим непустой файл:

```bash
echo "hello" > test10/not_empty.txt
```

Запускаем программу:

```bash
./empty_files.sh test10
```

Результат:

```text
empty1.txt
empty2.txt
```

`find` выполняет поиск файлов.

`-maxdepth 1` означает, что поиск выполняется только в указанной директории без перехода в подкаталоги.

`-type f` означает поиск обычных файлов.

`-name "*.txt"` оставляет только текстовые файлы с расширением `.txt`.

`-empty` оставляет только пустые файлы.


