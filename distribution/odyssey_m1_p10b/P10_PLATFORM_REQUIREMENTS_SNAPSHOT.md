# P10 Platform Requirements Snapshot

status: `PASS_P10B_OFFICIAL_REQUIREMENTS_SNAPSHOT`  
retrieved_at: `2026-08-28T00:00:00+08:00`  
authority: official platform documentation only

This is a dated release-engineering snapshot, not a perpetual rulebook. Recheck every platform immediately before submission.

## Apple Books

- accepted: EPUB; EPUB 3.3 supported; fixed layout supported
- cover: RGB high-quality JPEG/PNG; at least 1400 px on shorter axis
- metadata: title, author, language, Vendor ID and accurate customer-facing metadata; book file, cover and metadata must agree
- identifier: Vendor ID required; ISBN optional and should match Vendor ID when supplied
- validation: latest EPUBCheck plus Apple Books preview/submission validation
- fixed layout: EPUB 3 pre-paginated; consistent viewport; landmarks required when Apple-generated sample is used
- size boundary: ideally below 1 GB; Apple allows up to 2 GB
- external boundary: active Free or Paid Books Agreement and iTunes Connect/Publishing Portal action required
- official sources:
  - https://help.apple.com/itc/booksassetguide/en.lproj/static.html
  - https://itunespartner.apple.com/books/support/9-prepare-book
  - https://itunespartner.apple.com/books/support/12-metadata
  - https://itunespartner.apple.com/books/support/18-submit-your-book

## Google Play Books

- accepted: EPUB and PDF; EPUB 3.3 preferred; fixed-layout EPUB supported
- cover: JPEG, PNG, TIFF or PDF accepted in the single-book workflow; content/cover naming follows book identifier
- metadata: book settings, genre, contributors, description, territories and price are supplied in Partner Center
- identifier: ISBN is not required; Partner Center can issue a GGKEY
- validation: EPUBCheck and review as a Content Reviewer in Web Reader and, where possible, Android tablet app
- fixed layout: supported in EPUB 2/3; original-page PDF can be paired with EPUB
- size boundary: no universal ebook maximum stated in the cited official snapshot; processing status is authoritative after upload
- external boundary: Partner Center account, sales territories, payment profile, tax/bank and publish action remain manual
- official sources:
  - https://support.google.com/books/partner/answer/3316879?hl=en
  - https://support.google.com/books/partner/answer/9261664?hl=en
  - https://support.google.com/books/partner/answer/3431108?hl=en
  - https://support.google.com/books/partner/answer/107073?hl=en

## Kobo Writing Life

- accepted: EPUB accepted; fixed-layout EPUB is supported
- cover: portrait JPG/JPEG preferred or PNG; no larger than 5 MB; 300 DPI recommended; 3:4 suggested
- metadata: title, subtitle, series, series number, language, synopsis, categories and rights/distribution fields
- identifier: ISBN optional for Kobo direct; Kobo issues its own identifier, though partner distribution may require ISBN
- validation: error-free EPUB; test at least one eReader/desktop app and one phone/tablet; fixed-layout side-load suffix .fxl.kepub.epub
- fixed layout: supported, but fixed-layout titles do not receive Kobo Instant Preview
- size boundary: ebook content file maximum 100 MB
- external boundary: KWL account, rights, DRM, territories, pricing and publish action remain manual
- official sources:
  - https://kobowritinglife.zendesk.com/hc/en-us/articles/360058975732-Setting-up-a-New-eBook
  - https://kobowritinglife.zendesk.com/hc/en-us/articles/360059386271-File-Types-Sizes
  - https://kobowritinglife.zendesk.com/hc/en-us/articles/360058976112-Validating-and-Testing-Your-eBooks
  - https://kobowritinglife.zendesk.com/hc/en-us/articles/360059386031-ISBNs-and-Kobo-Writing-Life

## Amazon Kindle Direct Publishing

- accepted: EPUB or KPF for fixed-layout ebooks; MOBI is no longer accepted for fixed-layout ebooks
- cover: separate marketing cover; 2560 × 1600 px recommended, at least 300 PPI, JPEG preferred, 5 MB or less
- metadata: title/series/author on cover must match KDP metadata; categories, territories, pricing and rights are manual fields
- identifier: ISBN is not required for Kindle ebooks; Amazon assigns an ASIN
- validation: Kindle Previewer/Kindle Create preview; comic fixed-layout metadata and panel behavior must be checked
- fixed layout: graphic novels use fixed layout with image pop-ups/Panel View or Virtual Panels; book-type comic and original-resolution metadata required
- size boundary: no single maximum asserted by this snapshot; cover limit above is explicit
- external boundary: KDP account, rights declaration, marketplace, price/royalty, preview and publish action remain manual
- official sources:
  - https://kdp.amazon.com/en_US/help/topic/G9GSTY4LTRT39D4Z
  - https://kdp.amazon.com/en_US/help/topic/G200634390/
  - https://kdp.amazon.com/en_US/help/topic/G6GTK3T3NUHKLEFX
  - https://kdp.amazon.com/en_US/help/topic/G7DMSKCM9DVS65TC
