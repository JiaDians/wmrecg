import 'dart:convert';
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;
import 'package:wmrecg/result_info.dart';

enum SampleItem { watermelon, bottle }

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool is_record = false;
  bool is_need_send = false;
  String audioPath = "";
  String base64String = "";
  SampleItem? selectedMenu = SampleItem.watermelon;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title, style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.green,
        centerTitle: true,
      ),
      body: Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
        Text(
          "辨識結果說明",
          style: TextStyle(fontSize: 27, color: Colors.grey),
        ),
        Text(
          "越接近 100% → ${selectedMenu == SampleItem.watermelon ? "越新鮮" : "水瓶"}",
          style: TextStyle(fontSize: 22),
        ),
        Text(
          "越接近 0% → ${selectedMenu == SampleItem.watermelon ? "越成熟" : "空瓶"}",
          style: TextStyle(fontSize: 22),
        ),
        Expanded(
          child: (is_need_send == false)
              ? ((is_record == false)
                  ? Center(
                      child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Text('手機靠近${selectedMenu == SampleItem.watermelon ? "西瓜" : "水瓶"}', style: TextStyle(fontSize: 30)),
                        Text('按下方按鈕開始錄音', style: TextStyle(fontSize: 30))
                      ],
                    ))
                  : Center(
                      child: Text('錄音中...',
                          style:
                              TextStyle(fontSize: 30, color: Colors.orange))))
              : FutureBuilder(
                  future: send_data(base64String, selectedMenu!),
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      print('HasData');
                      String result_info = snapshot.data as String;
                      return Center(
                          child: ResultInfo(result_info: result_info));
                    } else if (snapshot.hasError) {
                      print('There was an error :(');
                      return Text('辨識失敗，請再試一次', style: TextStyle(fontSize: 30));
                    } else {
                      print('Circular');
                      return Container(
                        height: 50.0,
                        width: 50.0,
                        child: Center(
                          child: CircularProgressIndicator(
                            color: Colors.orange,
                          ),
                        ),
                      );
                    }
                  }),
        ),
        Expanded(
          child: Center(
            child: OutlinedButton(
                style: OutlinedButton.styleFrom(
                  padding: EdgeInsets.all(15),
                  side: (is_record == false)
                      ? BorderSide(width: 5.0, color: Colors.blue)
                      : BorderSide(width: 5.0, color: Colors.red),
                ),
                onPressed: () async {
                  debugPrint('Received click');
                  final record = Record();
                  if (is_record == false) {
                    if (await record.hasPermission()) {
                      Directory tempDir = await getTemporaryDirectory();
                      audioPath = '${tempDir.path}/record.wav';

                      await record.start(
                        numChannels: 1,
                        path: '$audioPath',
                        encoder: AudioEncoder.wav,
                        bitRate: 128000,
                        samplingRate: 16000,
                      );
                      setState(() {
                        is_record = true;
                        is_need_send = false;
                      });
                    }
                  } else {
                    await record.stop();
                    var fileBytes = await new File(audioPath).readAsBytes();

                    setState(() {
                      base64String = base64Encode(fileBytes);
                      is_record = false;
                      is_need_send = true;
                    });
                  }
                },
                child: (is_record == false)
                    ? Icon(
                        Icons.mic,
                        size: 75,
                        color: Colors.blue,
                      )
                    : Icon(
                        Icons.stop,
                        size: 75,
                        color: Colors.red,
                      )),
          ),
        ),
        Container(

          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: PopupMenuButton<SampleItem>(
              offset: Offset(1, 0),
              initialValue: selectedMenu,
              // Callback that sets the selected popup menu item.
              onSelected: (SampleItem item) {
                setState(() {
                  selectedMenu = item;
                });
              },
              itemBuilder: (BuildContext context) => <PopupMenuEntry<SampleItem>>[
                const PopupMenuItem<SampleItem>(
                  value: SampleItem.watermelon,
                  child: Text(
                    '西瓜',
                    style: TextStyle(fontSize: 20),
                  ),
                ),
                const PopupMenuItem<SampleItem>(
                  value: SampleItem.bottle,
                  child: Text(
                    '水瓶',
                    style: TextStyle(fontSize: 20),
                  ),
                ),
              ],
              child: ListTile(
                title: Text(
                  "選擇辨識項目 (${selectedMenu == SampleItem.watermelon ? "西瓜" : "水瓶"})",
                  style: TextStyle(fontSize: 25),
                ),
              ),
            ),
          ),
        ),
      ]),
    );
  }
}

Future<Object> send_data(String base64String, SampleItem selectedMenu) async {
  final response = await http.post(
    //Uri.parse('http://192.168.0.4:40251/submit'),
    Uri.parse('http://140.116.245.157:40251/submit'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'category': (selectedMenu == SampleItem.watermelon)? "watermelon" : "bottle",
      'data': base64String,
    }),
  );

  if (response.statusCode == 200) {
    print(response.statusCode.toString());
    return response.body;
  } else {
    print(response.statusCode.toString());
    throw Exception('Failed to request server.');
  }
}
