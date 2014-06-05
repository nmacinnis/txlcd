<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
  </head>
  <body style="font-family: 'courier';">
    <h1>
        current message: ${message}
    </h1>
    <h1>
        post a new message:
    </h1>
    <form action='/new' method='get'>
      <span>
        <input type='text' name='new_message' id='new_message' placeholder='important stuff' />
        <input type='submit' value='post' />
      </span>
    </form>
  </body>
</html>
