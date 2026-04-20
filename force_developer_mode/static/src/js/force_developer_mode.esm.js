import { browser } from "@web/core/browser/browser";
import { session } from "@web/session";
import { user } from "@web/core/user";

if (
  user.isAdmin &&
  !session.debug &&
  !window.location.search.includes("debug")
) {
  console.debug("Force Developer Mode: setting debug=1");
  const url = new URL(window.location.href);
  url.searchParams.set("debug", "1");
  browser.location.assign(url.toString());
}
