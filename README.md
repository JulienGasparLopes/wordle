# Wordle

This is a simple wordle game.

## Installation and running

- [Backend](./backend/README.md)
- [Frontend](./frontend/README.md)

## Setup Auth0

1. Create a new application in Auth0 (single-page application)
   1. Set the callback URL to `http://localhost:3000/api/auth/callback`
   2. Retrieve the secrets: `Domain`, `ClientID`, `Client Secret`
2. Create a new API in Auth0 with the identifier `https://wordle`
   1. Set the signing algorithm to `RS256`
   2. Set the signing key to `RS256`
