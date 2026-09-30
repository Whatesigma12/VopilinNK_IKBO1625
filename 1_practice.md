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

