> ⛔ ARŞİV (2026-07-28) — yürürlükte DEĞİL. LIFFY Faz 1a durum belgesi.
> ⚠️ PROVENANS: diskte kayıptı, Claude KB kopyasından yeniden üretildi; orijinaliyle bayt-bayt doğrulanmadı. İçindeki sayılar (80657/26123, owner UUID, dosya:satır) DOĞRULANMAMIŞ sayılır — LIFFY işine girilirken yeniden ölçülecek.
> Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# FAZ 1a — Durum Dökümanı (LIFFY Güvenlik İzolasyonu)

Tarih: 2026-06-08
Bağlam: ELL / LIFFY satışa hazırlama — güvenlik izolasyonu (Faz 1a)

---

## NEREDE KALDIK — TEK CÜMLE
1a'nın **şema ayağı bitti** (owner kolonu + backfill canlıya uygulandı, doğrulandı).
Sıradaki: **scope kodu** — ~12 sızan endpoint'e `reports_to` motorunu uygula.

---

## TAMAMLANAN (kanıtlı)

### Migration 048 — canlıya uygulandı ✅
- Dosya: `~/Projects/liffyv1/backend/migrations/048_add_sales_owner_user_id.sql`
- `persons`, `prospects`, `companies` tablolarına `sales_owner_user_id UUID`
  (FK → users.id, ON DELETE SET NULL, nullable) + her birine index eklendi.
- Backfill: tüm mevcut kayıtlar owner'a atandı.
  - owner id = `cfb66f28-54b1-4a82-85d5-616bb6bbd40b`
  - persons: 80657 / 80657 atandı ✅
  - prospects: 26123 / 26123 atandı ✅
  - companies: 0 kayıt (boş tablo, kolon hazır)
- Migration atomik (BEGIN/COMMIT), idempotent, owner-guard'lı (owner yoksa RAISE
  EXCEPTION + rollback). Canlı COMMIT alındı.
- Kolon adı `sales_owner_user_id` = locked B35 ile uyumlu (hedef Aşama 3 resolver
  bu alanı olduğu gibi kullanacak; resolver mantığı KURULMADI — o Aşama 3).

---

## KARARLAR (bu oturumda kanıta/locked'a bağlandı)

1. **Köprü = owner-scope, hedef = matrix (Aşama 3 / v4 Faz 4).**
   Köprüde basit owner-scope; resolver/iki-aşamalı mekanizma kurulmaz.
2. **Görünürlük kuralı:** rep kendi + altının verisini, yönetici altının hepsini
   görür (mevcut `reports_to` motoru). Requirements 359/138 + locked B33 uyumlu.
3. **Backfill = (a):** mevcut kayıtlar owner'a atandı (3 kullanıcı: owner/manager/
   sales_rep; havuz dağıtılmamış). UYGULANDI.
4. **`permissions` JSONB:** DOKUNMA. Ne köprünün ne hedefin parçası; prototipte
   zararsız, ELL'e geçişte ilişkisel `user_permissions` matrix'ine dönüşüp atılır.
   (locked özet satır 43 + B22/B30/B42 ile uyumlu.)
5. **Secret:** PARA RİSKİ YOK — Anthropic/SendGrid/ZeroBounce ne HEAD'de ne git
   geçmişinde sızmamış (Claude Code taraması). İki erişim-riski sızıntı var, ikisi
   de sona bırakıldı:
   - DB şifresi (CLAUDE_QUICKSTART.md, HEAD + 60 commit)
   - JWT dev-fallback `liffy_secret_key_change_me` (31 dosyada hardcoded)
   Karar: secret temizliği sistem kullanıma açılırken topluca yapılacak.

---

## SIRADAKİ — FAZ 1a SCOPE KODU (henüz YAPILMADI)

Mevcut `reports_to` motorunu (`getHierarchicalScope` / `canAccessRowHierarchical`
— middleware/userScope.js, zaten contactCrm'de çalışıyor; YENİ MOTOR YAZMA) şu
sızan endpoint'lere uygula:

### Düz scope eklenecek (list/detail/aggregate):
1. `routes/persons.js:33` — GET list
2. `routes/persons.js:483` — GET /:id
3. `routes/persons.js:559` — GET /:id/affiliations
4. `routes/persons.js:461` — GET /:id/campaigns
5. `routes/persons.js:169,188,230` — industries/companies/stats
6. `routes/leads.js:47` — GET list
7. `routes/prospects.js:115,192` — GET list + stats
8. `routes/companies.js:24,73,105,153` — list/count/industries/contacts
9. `routes/pipeline.js:215` — GET /board (assignee filtresi ekle)

### Özel muamele (düz scope DEĞİL):
10. `routes/persons.js:618` (+596 ön-kontrol) — DELETE /:id
    → scope + reason field (locked B12) + audit. Yıkıcı, öncelik.
11. `routes/persons.js:268` — GET /export
    → scope + "export capability" kontrolü (locked B42 iki-aşamalının köprü
      versiyonu; tam iki-aşamalı resolver Aşama 3).
12. `routes/pipeline.js:337` — null-assignee bypass'ını kapat
    (`if (currentAssignee && ...)` → assignee NULL olanı herkes claim edebiliyor).

### Gün-1 doğru desen (hafif):
- Yeni `sales_owner_user_id` yazımları + delete'ler `*_by_actor_type` + audit
  ile loglansın (locked B16). Köprüde hafif tut.

### DOKUNMA (Faz 4 / ayrı iş):
- `permissions` JSONB (yukarıda karar 4)
- legacy `team_ids` / `userScopeFilter` yetim plumbing (Faz 4 temizliği)
- `waiting.js:49,94` argüman sırası bug'ı (ilgisiz; non-privileged kullanıcıda
  bozuk SQL üretir — ayrı küçük fix, scope işiyle karıştırma)

---

## SCOPE KODU İÇİN ÖNEMLİ NOTLAR
- Scope eklerken kullanılacak kolon: `sales_owner_user_id` (artık üç tabloda var).
- `reports_to` motoru bu kolon üzerinden filtreleyecek (kişi kendi + altının
  sales_owner kayıtlarını görür).
- Önce READ-ONLY: her endpoint'in mevcut WHERE'ini görüp scope'u nasıl
  ekleyeceğini planlat, SONRA yazdır. Tek seferde 12'yi birden yazdırma — parça
  parça, test ederek.
- Smoke test (v4 1a gereği): iki test satışçısı birbirinin
  persons/leads/prospects/companies/pipeline verisini görememeli, export
  edememeli, silememeli. Manager ikisini de görmeli.
- Canlıya kod deploy AYRI onay gerektirir (v4 İlke 8).

---

## AÇIK KUYRUKLAR (Faz 1a dışı, unutma)
- LIFFY secret temizliği (DB şifresi rotation + JWT fallback) — sisteme açılırken.
- liffy-db IP kısıtı `0.0.0.0/0` açık — secret temizliğiyle birlikte.
- `liffy_user` (eski) hâlâ var — servisler v2'ye tam geçmeden SİLME.
- Migration ordering kırıklığı (005→007) — Faz 1'e ertelenmişti, hâlâ açık.

---

## ÇALIŞMA TARZI HATIRLATMASI (gelecek oturum için)
- Karar/öneri üretmeden önce: `ELAN_EXPO_REQUIREMENTS_v1_0.md` (ne lazım) +
  `ELL_LOCKED_KARARLAR_OZET.md` (mimari uyum) kontrol et. İkisi de knowledge base'de.
- Locked karara aykırı öneri çıkacaksa "bu locked'a aykırı" diye işaretle.
- Tahminle ilerleme; ölçülebilir şeyi Claude Code'a READ-ONLY saydır
  ("kodu değiştirme, dosya:satır kanıtı ver, bulamadığına 'bulamadım' de").
- Canlıya dokunan iş (deploy/migration/secret): önce analiz, dry-run, ayrı onay.
- Credential işleri kullanıcının kendi terminalinde; Render PSQL Command şifreyi
  gömülü verir.
