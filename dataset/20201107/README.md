以下を参考に分割しています<br>
[でかいファイルを分割＆結合するコマンド](https://qiita.com/seigot/items/622b3dd866aa3a51cf33)<br>

```
#分割
split -b 20m -a 2 _2020-11-05-01-45-29_2.zip _2020-11-05-01-45-29_2_p_

#結合
cat _2020-11-05-01-45-29_2_p_* > _2020-11-05-01-45-29_2.zip

#解凍
unzip _2020-11-05-01-45-29_2.zip
```
