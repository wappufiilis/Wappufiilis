output "table_name" {
  value = aws_dynamodb_table.time_series_data.name
}

output "per_guild_data_table_name" {
  value = aws_dynamodb_table.per_guild_data.name
}

output "per_year_data_table_name" {
  value = aws_dynamodb_table.per_year_data.name
}
