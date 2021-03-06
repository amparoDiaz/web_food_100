import tensorflow as tf, sys
from readcategory import readcategory


def classify(name):
	image_path = name
	readCategoryStruct=readcategory();
	result='''<H1>RESULTADO</H1> <table style="border: 1px;"> <tr>'''
	# Read in the image_data
	image_data = tf.gfile.FastGFile(image_path, 'rb').read()

	# Loads label file, strips off carriage return
	label_lines = [line.rstrip() for line 
		           in tf.gfile.GFile("tf_files/output_labels.txt")]

	# Unpersists graph from file
	with tf.gfile.FastGFile("tf_files/output_graph.pb", 'rb') as f:
	    graph_def = tf.GraphDef()
	    graph_def.ParseFromString(f.read())
	    _ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
	    # Feed the image_data as input to the graph and get first prediction
	    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	    
	    predictions = sess.run(softmax_tensor, \
		     {'DecodeJpeg/contents:0': image_data})
	    
	    # Sort to show labels of first prediction in order of confidence
	    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
	    resultNumber=0
	    #print readCategoryStruct
	    for node_id in top_k:
		human_string = label_lines[node_id]
		score = predictions[0][node_id]
		#print('%s (score = %.5f)' % (human_string, score))
		if(resultNumber==0):
			resultT= "<tr>"+  ('<td>%s </td> <td><mark>%s</mark> </td><td> (score = %.5f) </td>' % (human_string,readCategoryStruct[human_string], score)) +  '</tr>'

		else:
			resultT= "<tr>"+  ('<td>%s </td> <td>%s </td><td> (score = %.5f) </td>' % (human_string,readCategoryStruct[human_string], score)) +  '</tr>'
		result=result+resultT
		resultNumber=resultNumber+1
	    return result + '</table><frameset cols="25%,50%,25%"><frame src="frame_a.htm"></frameset> '

#classify('static/4.jpg')
