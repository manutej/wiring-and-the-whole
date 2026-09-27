public class SavingsController {
  public Page list(int p) { return svc.fetchPage(p); }
  public Dto get(long id) { return svc.fetchOne(id); }
  void log(String m) { audit.log(m); }
  // refs: savings.SavingsService#fetchPage savings.SavingsService#fetchOne shared.AuditDto#log shared.PageDto#of
}
