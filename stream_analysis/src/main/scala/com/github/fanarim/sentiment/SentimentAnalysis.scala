package com.github.fanarim.sentiment

import edu.stanford.nlp.pipeline.StanfordCoreNLP
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations
import edu.stanford.nlp.ling.CoreAnnotations
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations
import java.util.Properties
import scala.collection.JavaConversions._

object SentimentAnalysis {
  def getAverageSentiment(text: String) : Double = {
    val prop = new Properties()
    prop.setProperty("annotators", "tokenize, ssplit, pos, lemma, parse, sentiment")

    val pipeline = new StanfordCoreNLP(prop);

    var charCount = 0
    var sentimentCharsSum = 0

    if (text.length() != 0){
      val annotation = pipeline.process(text);

      for (sentence <- annotation.get(classOf[CoreAnnotations.SentencesAnnotation])){
        charCount += sentence.toString().length()
        val tree = sentence.get(classOf[SentimentCoreAnnotations.SentimentAnnotatedTree])
        val sentiment = RNNCoreAnnotations.getPredictedClass(tree)
        sentimentCharsSum += sentence.toString().length() * sentiment
      }
    }

    return sentimentCharsSum.toFloat/charCount
  }
}
