output "api_url" {
  value = aws_apigatewayv2_stage.default.invoke_url
}

output "dynamodb_table" {
  value = aws_dynamodb_table.visitor_count.name
}

output "lambda_function" {
  value = aws_lambda_function.visitor_counter.function_name
}