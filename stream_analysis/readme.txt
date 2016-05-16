NAVOD PRO SPUSTENI
------------------

0. nastaveni udaju k databazi v souboru db_cred.txt

1. vytvoreni spustitelneho jaru
$ cd stream_analysis
$ JAVA_OPTS=-Xmx1524M sbt assembly

2. vytvoreni spark ulohy
$ ($spark_dir)/bin/spark-submit --class com.github.fanarim.TwitterWishesAnalysis --executor-memory 8G --executor-cores 3 --master local[*] target/scala-2.10/Tweets_stream_analysis-assembly-0.1.jar
