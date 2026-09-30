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
## Task 4
Написать программу для вывода всех идентификаторов из файла без повторений.

терминал:
```bash
nano identifiers
```

nano:
```
#!/bin/bash

grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u
```
Даем право на выполнение:

```bash
chmod +x identifiers
```

Запуск:

```bash
./identifiers hello.c
```

Объяснение: `grep` находит в файле слова, которые могут быть идентификаторами программы, а `sort -u` сортирует их и удаляет повторения.

---

## Task 5

Написать программу для регистрации пользовательской команды.

терминал:

```bash
nano reg
```

nano:

```bash
#!/bin/bash

chmod 755 "$1"
sudo cp "$1" /usr/local/bin/
```

Даем право на выполнение:

```bash
chmod +x reg
```

Например, регистрируем программу banner:

```bash
./reg banner
```

Теперь программу можно запускать просто командой:

```bash
banner "Hello"
```

Объяснение: `chmod 755` дает программе право на выполнение, а `cp` копирует ее в `/usr/local/bin`. Программы из этой папки можно запускать как обычные команды Linux.

---

## Task 6

Написать программу для проверки комментария в первой строке файлов `.c`, `.js` и `.py`.

терминал:

```bash
nano comments
```

nano:

```bash
#!/bin/bash

for file in *.c *.js *.py
do
    if [ -f "$file" ]; then
        if head -n 1 "$file" | grep -Eq '^[[:space:]]*(//|/\*|#)'; then
            echo "$file - комментарий есть"
        else
            echo "$file - комментария нет"
        fi
    fi
done
```

Даем право на выполнение:

```bash
chmod +x comments
```

Запуск:

```bash
./comments
```

Объяснение: программа перебирает файлы `.c`, `.js` и `.py`. Команда `head -n 1` берет только первую строку, а `grep` проверяет, начинается ли она с `//`, `/*` или `#`.

---

## Task 7

Написать программу для поиска файлов-дубликатов в указанной директории и ее подкаталогах.

терминал:

```bash
nano duplicates
```

nano:

```bash
#!/bin/bash

find "$1" -type f -exec md5sum {} + | sort | uniq -w 32 -D | cut -c 35-
```

Даем право на выполнение:

```bash
chmod +x duplicates
```

Запуск:

```bash
./duplicates .
```

Объяснение: `find` находит файлы, `md5sum` считает контрольную сумму каждого файла. Если у двух файлов одинаковое содержимое, их контрольные суммы будут одинаковыми. `uniq` оставляет такие совпадения.

---

## Task 8

Написать программу, которая находит файлы с указанным расширением и помещает их в tar-архив.

терминал:

```bash
nano archive
```

nano:

```bash
#!/bin/bash

find "$1" -type f -name "*.$2" > files.txt
tar -cf archive.tar -T files.txt
rm files.txt
```

Даем право на выполнение:

```bash
chmod +x archive
```

Например, архивируем все `.txt` файлы:

```bash
./archive . txt
```

Будет создан файл:

```text
archive.tar
```

Объяснение: первый аргумент - папка, второй - расширение. `find` ищет подходящие файлы, а `tar` складывает их в архив `archive.tar`.

---

## Task 9

Написать программу для замены четырех пробелов на символ табуляции.

терминал:

```bash
nano spaces
```

nano:

```bash
#!/bin/bash

sed 's/    /\t/g' "$1" > "$2"
```

Даем право на выполнение:

```bash
chmod +x spaces
```

Запуск:

```bash
./spaces input.txt output.txt
```

Объяснение: `$1` - исходный файл, `$2` - новый файл. `sed` ищет последовательности из четырех пробелов и заменяет их на табуляцию.

---

## Task 10

Написать программу для вывода названий всех пустых файлов в указанной директории.

терминал:

```bash
nano empty
```

nano:

```bash
#!/bin/bash

find "$1" -maxdepth 1 -type f -empty
```

Даем право на выполнение:

```bash
chmod +x empty
```

Запуск:

```bash
./empty .
```

Объяснение: `find` проверяет указанную директорию. `-type f` означает обычные файлы, а `-empty` оставляет только пустые файлы.


