
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class SalesBreakdown {

    public static class SalesMapper
            extends Mapper<Object, Text, Text, DoubleWritable> {

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String[] fields = value.toString().split(",");

            if (fields.length != 8) {
                return;
            }

            try {
                String category = fields[3].trim();
                String region = fields[7].trim();

                double quantity =
                        Double.parseDouble(fields[4].trim());
                double price =
                        Double.parseDouble(fields[5].trim());

                double revenue = quantity * price;

                context.write(
                        new Text("CATEGORY:" + category),
                        new DoubleWritable(revenue));

                context.write(
                        new Text("REGION:" + region),
                        new DoubleWritable(revenue));

            } catch (NumberFormatException e) {
                // Skip invalid rows
            }
        }
    }

    public static class SalesReducer
            extends Reducer<Text, DoubleWritable,
                            Text, DoubleWritable> {

        public void reduce(Text key, Iterable<DoubleWritable> values,
                           Context context)
                throws IOException, InterruptedException {

            double total = 0;

            for (DoubleWritable value : values) {
                total += value.get();
            }

            context.write(key, new DoubleWritable(total));
        }
    }

    public static void main(String[] args) throws Exception {

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Category and Region Sales");

        job.setJarByClass(SalesBreakdown.class);
        job.setMapperClass(SalesMapper.class);
        job.setCombinerClass(SalesReducer.class);
        job.setReducerClass(SalesReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
