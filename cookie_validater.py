import json
import requests
import tldextract

file_name = 'cookiebro-cookies.json' # cookies exported by [CookieBro](https://chromewebstore.google.com/detail/cookiebro/lpmockibcakojclnfmhchibmdpmollgn)
keywords = ( 'd0gkiller87' ) # keywords only exist in authenticated response (e.g. your nickname)
timeout_sec = 5 # seconds to wait before connection timeout

def search_keyword( response ):
  for keyword in keywords:
    if keyword.lower() in response.lower():
      return keyword
  return False

def load_cookies( cookies: dict ):
  domains = {}
  for cookie in cookies:
    domain_name = '.'.join(
      tldextract.extract(
        cookie['domain'].strip( '.' )
      )[1:]
    )
    if domain_name not in domains:
      domains[domain_name] = {}
    domains[domain_name][cookie['name']] = cookie['value']
  return domains

def main():
  cookies = json.load( open( file_name ) )
  domains = load_cookies( cookies )
  print( 'Cookies loaded.' )

  domain_lens = len( domains )
  i = 1

  for domain_name in domains:
    # replace insecured http:// protocol with https://
    scheme = 'https://'
    try:
      print(
        f"[*] Testing[{ i }/{ domain_lens }] { scheme + domain_name } ...",
        end=''
      )
      r = requests.get(
        scheme + domain_name,
        cookies = domains[domain_name],
        allow_redirects = True,
        timeout = timeout_sec
      )
      found = search_keyword( r.text )
      if found:
        print( f"\n\033[6;30;42m[+] Valid session found:\033[1;33;40m { domain_name } ({ found })\033[0m" )
      else:
        # nothing interesting found
        print( '' )
    except KeyboardInterrupt:
      print( '' )
      return
    except Exception as e:
      # mostly caused by connetion errors
      print( '\033[1;31;40m failed\033[0m' )
    i += 1

if __name__ == '__main__':
  main()
