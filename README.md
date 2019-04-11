[![Build Status](https://travis-ci.org/Omulosi/catalog.svg?branch=master)](https://travis-ci.org/Omulosi/catalog)
[![Coverage Status](https://coveralls.io/repos/github/Omulosi/catalog/badge.svg?branch=master)](https://coveralls.io/github/Omulosi/catalog?branch=master)

Catalog API
================

This API exposes data displayed and used by the Catalog application. The API complies
with REST standards and the JSON API  specification.

## Authentication
Catalog API uses API access tokens to allow access to the API. You can generate
a new token by either signing in or signing up for the API.

Catalog expects for the access token to be included in all requests to protected
endpoints in a header that looks like the following (replace {TOKEN} with your own).

```
	Authentication: Bearer {TOKEN}
```
