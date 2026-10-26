
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

public class ProductRevenue {

    public static class RevenueMapper
            extends Mapper<Object, Text, Text, DoubleWritable> {

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();
            String[] fields = line.split(",");

            if (fields.length != 8) {
                return;
            }

            try {
                String product = fields[2].trim();
                double quantity = Double.parseDouble(fields[4].trim());
                double price = Double.parseDouble(fields[5].trim());

                double revenue = quantity * price;

                context.write(new Text(product),
                              new DoubleWritable(revenue));
            } catch (NumberFormatException e) {
                // Skip invalid rows
            }
        }
    }

    public static class RevenueReducer
            extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {

        public void reduce(Text product, Iterable<DoubleWritable> values,
                           Context context)
                throws IOException, InterruptedException {

            double total = 0;

            for (DoubleWritable value : values) {
                total += value.get();
            }

            context.write(product, new DoubleWritable(total));
        }
    }

    public static void main(String[] args) throws Exception {

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Product Wise Revenue");

        job.setJarByClass(ProductRevenue.class);
        job.setMapperClass(RevenueMapper.class);
        job.setCombinerClass(RevenueReducer.class);
        job.setReducerClass(RevenueReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
