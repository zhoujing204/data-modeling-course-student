msg = "Hello World"
msg1 = "Hello"
msg2 = "World"
msg3 = msg1 + " " + msg2

msg_id = id(msg)
msg3_id = id(msg3)

print(msg_id == msg3_id)
# explain why msg_id not equal to msg3_id
# msg_id is the id of the original string "Hello World"
# msg3_id is the id of the new string "Hello World"
# so msg_id not equal to msg3_id
