package com.linkedin.feathr.offline.generation

import com.linkedin.feathr.offline.source.dataloader.hdfs.FileFormat
import org.apache.avro.generic.GenericRecord
import org.apache.hadoop.mapred.JobConf
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, SaveMode}

object SparkIOUtils {
  def createUnionDataFrame(existingHdfsPaths: Seq[String], dataIOParameters: Map[String, String] = Map()): DataFrame = {
    // existingHdfsPaths may be folder or file with suffix
    // Currently only support parquet file but not folder with parquet files
    val format = FileFormat.getTypeForUnionDF(existingHdfsPaths, dataIOParameters)
    FileFormat.loadHdfsDataFrame(format, existingHdfsPaths)
  }

  def createDataFrame(path: String, dataIOParams: Map[String, String] = Map()): DataFrame = {
    createUnionDataFrame(Seq(path), dataIOParams)
  }

  def writeDataFrame(outputDF: DataFrame, path: String, parameters: Map[String, String] = Map()): DataFrame = {
    outputDF.write.mode(SaveMode.Overwrite).format("avro").save(path)
    outputDF
  }

  def createGenericRDD(inputPath: String, dataIOParameters: Map[String, String], jobConf: JobConf): RDD[GenericRecord] = ???

  val OUTPUT_SCHEMA = "output.schema"
  val DATA_FORMAT = "data.format"
  val OUTPUT_PARALLELISM = "output.parallelism"
  val SPLIT_SIZE = "split.size"
  val OVERWRITE_MODE = "override.mode"
  val FILTER_EXP = "filter.exp"
}
