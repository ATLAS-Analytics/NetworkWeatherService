package edu.uchicago.networkweather;

import java.io.IOException;
import java.nio.charset.Charset;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.TimeZone;

import org.apache.commons.lang.time.FastDateFormat;
import org.apache.flume.Context;
import org.apache.flume.Event;
import org.apache.flume.conf.ComponentConfiguration;
import org.apache.flume.sink.elasticsearch.AbstractElasticSearchIndexRequestBuilderFactory;
import org.elasticsearch.action.index.IndexRequestBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyESindexRequestBuilderFactory extends AbstractElasticSearchIndexRequestBuilderFactory {
	
	private static final Logger LOG = LoggerFactory.getLogger(MyESindexRequestBuilderFactory.class);
	final Charset charset = Charset.forName("UTF-8");
    TimeZone tz = TimeZone.getTimeZone("UTC");
    DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm'Z'");
    
	public MyESindexRequestBuilderFactory() {
		super(FastDateFormat.getInstance("yyyy.MM.dd", TimeZone.getTimeZone("Etc/UTC")));
	}

	public MyESindexRequestBuilderFactory(FastDateFormat fd) {
		super(fd);
	}

	@Override
	protected void prepareIndexRequest(IndexRequestBuilder indexRequest, String indexName, String indexType, Event event) throws IOException {
//		LOG.debug("event: "+ event.toString());

		Map<String, Object> source = new HashMap<String, Object>(8);
		
//	    df.setTimeZone(tz);
//	    String nowAsISO = df.format(new Date());
		
		Map<String,String> headers=event.getHeaders();
		for (String key : headers.keySet()) {
			LOG.debug("header:"+key+"  v: "+headers.get(key));
			if (key.equals("timestamp")){
				Long ts= Long.parseLong(headers.get(key));
				source.put("timestamp", new Date(ts));
			}
			else if(key.contains("Production")){
				if (headers.get(key).equalsIgnoreCase("true")){
					source.put(key, new Boolean(true));
				}
				else{
					source.put(key, new Boolean(false));
				}
			}
			else if (key.equals("throughput")){
				Float thr=Float.parseFloat(headers.get(key));
				source.put(key, thr);
			}
			else{
				source.put(key, headers.get(key));
			}
		}
		
		indexRequest.setIndex(indexName).setType(indexType).setSource(source);
	}

	@Override
	public void configure(Context arg0) {
	}

	@Override
	public void configure(ComponentConfiguration arg0) {
	}

}