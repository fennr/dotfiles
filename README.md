# bspwm dotfiles##ОбзорОбзорные скриншоты конфига.<img src='/images/scrot.png'><img src='/images/code.png'><img src='/images/rofi.png'>##УстановкаДля установки базовой комплектации выполните скрипт* instal-minimal.shПри этом будет установлено следующее* bspwm* lemonbar-xft (AUR)* sxhkd* rofi* font-awesome (AUR)* zsh* byobu* lm_sensors* comptonПосле запустите скрипт распаковки конфигурации запустив dot.shПосле чего настройте запуск bspwm в конфигурации вашего DM или конфигурации запуска иксервера.##НастройкаВ конфиге в качестве панели используется lemonbar с его инициализацией могут возникнуть проблемыТут разъясняется как справиться с той или иной проблемой редактируя фаил .lemon.py (по мере поступления жалоб список будет пополняться).Вид панели:<img src='/images/panel.png'>###Если панели нетЕсли вы не наблюдаете панель после запуска, не паникуйте, откройте файл bspwmrc по пути /home/user-neme/.config/bspwm , и в 47 строке необходимо указать свою ширину монитора	< ~/./.reader.sh | lemonbar -f "fontawesome:size=18" -f "Cantarell:size=14" -g 1255x30+10+8 -p -u 4 & >Заменяя значение 1255Так же в этом же файле укажите полный путь к изображению, которое вы хотели бы видеть на рабочем столе изменив строку 46.###Теги<img src='/images/tag.png'>В окружении иcпользуеться система тегов, для навигации по ним, а так же для управления/премещения окон используйте хоткеи:* super + {1-7} -  Переключение тегов (1-7)* super + shift + {1-7} - Перемещение активного окна не тег (1-7)* alt + Tab - Переключение активного окна* alt + q - Закрытие активного окнаПолный список хоткеев вы найдете в файле sxhkd который находиться по пути /home/user-neme/.config/sxhkd .###Дата<img src='/images/time.png'>Если у вас смещены значения или неправильно отображается время и дата, необходимо поправить начало и конец сбора данных в файле .lemon.py >Строки под номером 31 и 32	< def get_time():       raw = run("date")[:16]       return raw[:10] + "," + raw[10:] >>Заменяем значения "16, 10,10" на свои.###Сеть<img src='/images/net.png'>При неполном, или неправильном отображении названия вашей сети, либо если отсутствует необходимость в ее отображении редактируйте файл  .lemon.py >Строки под номером 71-74	< def wifi():        raw = run(["iwgetid"]).splitlines()[0][17:-1]         if "ff" in raw: return ""         return WIFI + " " + raw + "  "  >>Заменяем значения "17, -1" на свои.>А для удаления комментируем этот блок и в строке 99 удаляем wifi().###Батарейка<img src='/images/bat.png'>При не отображении индикатора, либо если нет необходимости в нем, изменяем файл  .lemon.py >Строки под номером 76-96	<  def battery():         raw     = run(["acpi"])[11:-1]         icon    = ""         if "until" in raw:           if   percent <= 5:   icon = WIRED + " " +  B_CRITICAL           elif percent <= 25:  icon = WIRED + " " + B_LOW           elif percent <= 50:  icon = WIRED + " " + B_HALF           elif percent <= 75:  icon = WIRED + " " + B_ALMOST           elif percent <= 100: icon = WIRED + " " + B_FULL         elif "Full" in raw:           icon = WIRED         elif "remaining" in raw:           percent = int(raw[raw.find(" ")+1:raw.find("%")])           if   percent <= 5:   icon = B_CRITICAL           elif percent <= 25:  icon = B_LOW           elif percent <= 50:  icon = B_HALF           elif percent <= 75:  icon = B_ALMOST           elif percent <= 100: icon = B_FULL           icon += " "           if icon == B_LOW + " ": return RED + icon         return icon  >>Заменяем значения "11, -1" на свои.>А для удаления комментируем этот блок и в строке 99 удаляем battery().##ХоткеиВ скрипте используются хоткеи вот базовые из них.* super + shift + Escape   -   Выключение системы* super + shift + grave    -   Перезагрузка* super + l        -   Блокировка (если стоит i3lock)* ctrl + space  -   Смена раскладки (us/ru)* super + r        -   Вызов rofi (контекстное меню для запуска программ)Остальные команды, а также их изменение (либо смена программ которые активируються) вы найдете в файле sxhkd который находиться по пути /home/user-neme/.config/sxhkd .