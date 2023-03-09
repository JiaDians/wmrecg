import 'package:flutter/cupertino.dart';

class ResultInfo extends StatefulWidget {
  final result_info;

  const ResultInfo({Key? key, this.result_info}) : super(key: key);

  @override
  State<ResultInfo> createState() => _ResultInfoState();
}

class _ResultInfoState extends State<ResultInfo> {
  final result_info;

  _ResultInfoState({this.result_info});

  @override
  Widget build(BuildContext context) {
    return Text(widget.result_info, style: TextStyle(fontSize: 40));
  }
}
